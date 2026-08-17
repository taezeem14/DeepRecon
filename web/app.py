"""FastAPI Web UI and REST API server for DeepRecon."""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import (
    AI_PROVIDER,
    CRAWL_DELAY,
    CRAWL_DEPTH,
    CRAWL_WORKERS,
    DB_PATH,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    TOR_PROXY,
)
from core.ai_analyzer import AIAnalyzer
from core.crawler import AsyncCrawler
from core.reporter import ReportGenerator
from core.search_engines import AsyncMetaSearch
from storage.db import DeepReconDB
from utils.tor_manager import TorManager, renew_ip

app = FastAPI(title="DeepRecon Web Dashboard", version="3.2.0")

template_dir = Path(__file__).resolve().parent / "templates"
template_dir.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(template_dir))
db = DeepReconDB(DB_PATH)
tor_manager = TorManager()
ai_analyzer = AIAnalyzer()


def _crawl_task(seed_url: str, session_id: int) -> None:
    """Background task executing the async crawler."""
    crawler = AsyncCrawler(
        db=db,
        depth=CRAWL_DEPTH,
        workers=CRAWL_WORKERS,
        delay=CRAWL_DELAY,
        timeout=REQUEST_TIMEOUT,
        proxy_url=TOR_PROXY,
        max_retries=MAX_RETRIES,
    )
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(crawler.crawl([seed_url]))
    finally:
        loop.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sessions = db.list_sessions()
    tor_ip = tor_manager.get_current_ip() or "Offline / Proxy Unreachable"
    total_pages = db.count_rows("pages")
    total_links = db.count_rows("links")
    total_keywords = db.count_rows("keywords_found")
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sessions": sessions,
            "tor_ip": tor_ip,
            "ai_provider": AI_PROVIDER.upper(),
            "total_pages": total_pages,
            "total_links": total_links,
            "total_keywords": total_keywords,
        },
    )


@app.post("/scan")
async def start_scan(
    request: Request,
    background_tasks: BackgroundTasks,
    url: str = Form(...),
    session_name: str = Form(...),
):
    try:
        session_id = db.create_session(session_name, seed_url=url)
    except Exception:
        session_name = f"{session_name}_{int(time.time())}"
        session_id = db.create_session(session_name, seed_url=url)

    background_tasks.add_task(_crawl_task, url, session_id)

    sessions = db.list_sessions()
    tor_ip = tor_manager.get_current_ip() or "Offline / Proxy Unreachable"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "sessions": sessions,
            "tor_ip": tor_ip,
            "ai_provider": AI_PROVIDER.upper(),
            "message": f"Async crawl initiated for {url} in session '{session_name}' (ID: {session_id})!",
            "total_pages": db.count_rows("pages"),
            "total_links": db.count_rows("links"),
            "total_keywords": db.count_rows("keywords_found"),
        },
    )


@app.get("/search", response_class=HTMLResponse)
async def search_pages(request: Request, q: str = ""):
    results = []
    if q:
        results = db.search_pages(q, limit=30)

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "query": q,
            "results": results,
            "tor_ip": tor_manager.get_current_ip() or "Offline",
        },
    )



@app.post("/api/metasearch")
async def api_metasearch(query: str = Form(...)):
    """API endpoint to execute Dark Web multi-engine meta-search."""
    meta = AsyncMetaSearch()
    results = await meta.search(query)
    return JSONResponse({"query": query, "count": len(results), "results": results})


@app.post("/api/ai_summary")
async def api_ai_summary(session_id: int = Form(...)):
    """API endpoint to synthesize an investigation summary via AI."""
    session = db.get_session(session_id)
    if not session:
        return JSONResponse({"error": "Session not found"}, status_code=404)

    pages = db.list_pages(session_id)
    if not pages:
        return JSONResponse({"error": "No pages in session to analyze"}, status_code=400)

    target_page = pages[0]
    summary = ai_analyzer.generate_investigation_summary(
        target_page["url"],
        target_page.get("content", ""),
        target_page.get("meta", {}),
    )
    return JSONResponse({"session_id": session_id, "url": target_page["url"], "summary": summary})


@app.post("/api/tor/renew")
async def api_tor_renew():
    """Request a fresh Tor exit circuit."""
    success = renew_ip()
    new_ip = tor_manager.get_current_ip() or "Unknown"
    return JSONResponse({"success": success, "tor_ip": new_ip})


def start_web_ui(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Launch the Web Dashboard."""
    uvicorn.run("web.app:app", host=host, port=port, reload=False)
