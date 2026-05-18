"""Rich CLI entry point for DeepRecon."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from config import CRAWL_DELAY, CRAWL_DEPTH, CRAWL_WORKERS, DB_PATH, MAX_RETRIES, REQUEST_TIMEOUT, TOR_PROXY
from core.crawler import AsyncCrawler, crawl_recursive
from core.reporter import ReportGenerator
from core.searcher import Searcher
from storage.db import DeepReconDB
from utils.logger import configure_logging
from utils.tor_manager import TorManager, renew_ip
from utils.validator import is_onion_url, sanitize_url


console = Console()


def _timestamp_name(prefix: str) -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"


def _show_banner(tor_manager: TorManager) -> None:
    current_ip = tor_manager.get_current_ip() or "unknown"
    console.print(
        Panel.fit(
            f"[bold]DeepRecon[/bold]\nTor IP: {current_ip}\nDatabase: {DB_PATH}",
            title="DeepRecon",
            border_style="cyan",
        )
    )


def _print_sessions(db: DeepReconDB) -> None:
    sessions = db.list_sessions()
    table = Table(title="Sessions")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Seed URL")
    table.add_column("Status")
    table.add_column("Started")
    for session in sessions:
        table.add_row(
            str(session["id"]),
            session["name"],
            session.get("seed_url") or "",
            session.get("status") or "",
            session.get("started_at") or "",
        )
    console.print(table)


def _crawl_site(db: DeepReconDB) -> int | None:
    url = sanitize_url(Prompt.ask("Seed URL (.onion or clearnet)"))
    if is_onion_url(url):
        console.print("[green]Validated onion target.[/green]")
    elif not Confirm.ask("Target is not an onion URL. Continue anyway?", default=False):
        return None

    session_name = Prompt.ask("Session name", default=_timestamp_name("session"))
    try:
        session_id = db.create_session(session_name, seed_url=url)
    except Exception:
        session_name = _timestamp_name("session")
        session_id = db.create_session(session_name, seed_url=url)

    crawler = AsyncCrawler(
        db=db,
        depth=CRAWL_DEPTH,
        workers=CRAWL_WORKERS,
        delay=CRAWL_DELAY,
        timeout=REQUEST_TIMEOUT,
        proxy_url=TOR_PROXY,
        max_retries=MAX_RETRIES,
    )

    console.print(f"Starting crawl for session [bold]{session_name}[/bold]...")
    with console.status("Crawling targets...", spinner="dots"):
        try:
            asyncio.run(crawler.crawl([url]))
        except RuntimeError:
            links = crawl_recursive(url, depth=CRAWL_DEPTH)
            page_id = db.upsert_page(
                {
                    "site_id": db.get_or_create_site(url, title=None),
                    "session_id": session_id,
                    "url": url,
                    "title": url,
                    "content": "",
                    "raw_html": "",
                    "meta": {"links": links},
                }
            )
            if links:
                db.add_links(page_id, url, [{"target_url": link, "is_internal": True} for link in links])

    console.print(f"[green]Crawl finished for session {session_id}.[/green]")
    return session_id


def _search_pages(db: DeepReconDB) -> None:
    query = Prompt.ask("Search query")
    use_regex = Confirm.ask("Treat the query as regex?", default=False)
    limit = IntPrompt.ask("Max results", default=10)

    if use_regex:
        searcher = Searcher()
        pages = db.list_pages()
        matches = []
        for page in pages:
            content = page.get("content") or ""
            matches.extend(searcher.search_text(content, [query], regex=True))
        if not matches:
            console.print("[yellow]No regex matches found.[/yellow]")
            return

        table = Table(title="Regex Matches")
        table.add_column("Keyword")
        table.add_column("Match")
        table.add_column("Context")
        for match in matches[:limit]:
            table.add_row(match.keyword, match.match_text, match.context)
        console.print(table)
        return

    results = db.search_pages(query, limit=limit)
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        return

    table = Table(title="Search Results")
    table.add_column("URL", style="cyan")
    table.add_column("Title")
    table.add_column("Language")
    table.add_column("Score")
    for row in results:
        table.add_row(
            row.get("url", ""),
            row.get("title") or "",
            row.get("language") or "",
            str(row.get("relevance_score", 0.0)),
        )
    console.print(table)


def _generate_report(db: DeepReconDB) -> None:
    session_id = IntPrompt.ask("Session ID")
    generator = ReportGenerator(db=db)
    outputs = generator.generate_session_report(session_id)
    console.print(f"[green]Report written:[/green] {outputs['html']}")
    console.print(f"[green]JSON written:[/green] {outputs['json']}")
    if "pdf" in outputs:
        console.print(f"[green]PDF written:[/green] {outputs['pdf']}")


def main() -> None:
    """Run the interactive DeepRecon CLI or Web UI."""
    import argparse
    parser = argparse.ArgumentParser(description="DeepRecon OSINT Framework")
    parser.add_argument("--web", action="store_true", help="Launch the Web UI")
    parser.add_argument("--cli", action="store_true", help="Launch the interactive CLI (default)")
    parser.add_argument("--host", default="127.0.0.1", help="Host for Web UI")
    parser.add_argument("--port", type=int, default=8000, help="Port for Web UI")
    args = parser.parse_args()

    configure_logging()
    
    if args.web and not args.cli:
        console.print(f"[bold green]Starting Web UI at http://{args.host}:{args.port}[/bold green]")
        import uvicorn
        uvicorn.run("web.app:app", host=args.host, port=args.port, reload=False)
        return

    db = DeepReconDB(DB_PATH)
    tor_manager = TorManager()
    _show_banner(tor_manager)

    while True:
        console.print("\n[bold cyan]1[/bold cyan] Crawl target")
        console.print("[bold cyan]2[/bold cyan] Search stored pages")
        console.print("[bold cyan]3[/bold cyan] Renew Tor IP")
        console.print("[bold cyan]4[/bold cyan] Generate session report")
        console.print("[bold cyan]5[/bold cyan] List sessions")
        console.print("[bold cyan]6[/bold cyan] Exit")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            _crawl_site(db)
        elif choice == "2":
            _search_pages(db)
        elif choice == "3":
            if renew_ip():
                console.print("[green]Tor identity renewal requested.[/green]")
            else:
                console.print("[red]Unable to renew Tor identity.[/red]")
        elif choice == "4":
            _generate_report(db)
        elif choice == "5":
            _print_sessions(db)
        elif choice == "6":
            console.print("Exiting DeepRecon.")
            break


if __name__ == "__main__":
    main()
