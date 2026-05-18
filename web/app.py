import os
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio

from storage.db import DeepReconDB
from config import DB_PATH, CRAWL_DEPTH, CRAWL_WORKERS, CRAWL_DELAY, REQUEST_TIMEOUT, TOR_PROXY, MAX_RETRIES
from core.crawler import AsyncCrawler
from core.searcher import Searcher
from utils.tor_manager import TorManager

app = FastAPI(title="DeepRecon Web UI")

# Make sure we have a templates folder
template_dir = os.path.join(os.path.dirname(__file__), "templates")
if not os.path.exists(template_dir):
    os.makedirs(template_dir)

templates = Jinja2Templates(directory=template_dir)
db = DeepReconDB(DB_PATH)
tor_manager = TorManager()


def crawl_task(seed_url: str, session_id: int):
    # This runs asynchronously in background
    crawler = AsyncCrawler(
        db=db,
        depth=CRAWL_DEPTH,
        workers=CRAWL_WORKERS,
        delay=CRAWL_DELAY,
        timeout=REQUEST_TIMEOUT,
        proxy_url=TOR_PROXY,
        max_retries=MAX_RETRIES,
    )
    # The crawler requires an active loop. Since we're in a FastAPI background task which runs in a thread pool,
    # we need to create a new event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(crawler.crawl([seed_url]))
    finally:
        loop.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    sessions = db.list_sessions()
    tor_ip = tor_manager.get_current_ip() or "unknown"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "sessions": sessions,
        "tor_ip": tor_ip
    })


@app.post("/scan")
async def start_scan(request: Request, background_tasks: BackgroundTasks, url: str = Form(...), session_name: str = Form(...)):
    try:
        session_id = db.create_session(session_name, seed_url=url)
    except Exception:
        import time
        session_name = f"{session_name}_{int(time.time())}"
        session_id = db.create_session(session_name, seed_url=url)

    background_tasks.add_task(crawl_task, url, session_id)
    
    sessions = db.list_sessions()
    tor_ip = tor_manager.get_current_ip() or "unknown"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "sessions": sessions,
        "tor_ip": tor_ip,
        "message": f"Scan started successfully for {url} in session {session_name}!"
    })


@app.get("/search", response_class=HTMLResponse)
async def search_pages(request: Request, q: str = ""):
    results = []
    if q:
        results = db.search_pages(q, limit=20)
    
    return templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "results": results
    })


def start_web_ui(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run("web.app:app", host=host, port=port, reload=True)
