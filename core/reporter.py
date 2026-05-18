"""Report generation for DeepRecon."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Iterable

try:
    from weasyprint import HTML
except ImportError:  # pragma: no cover - optional dependency
    HTML = None

from config import ENABLE_PDF_EXPORT, REPORTS_PATH
from core.parser import PageData
from storage.db import DeepReconDB
from utils.logger import get_logger


LOGGER = get_logger(__name__)
DISCLAIMER = (
    "Ethical use only: DeepRecon is intended for authorized security research, "
    "threat intelligence, and defensive investigations."
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _as_dict(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return dict(value)
    raise TypeError("Expected a mapping or dataclass instance")


def _render_table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    thead = "".join(f"<th>{escape(header)}</th>" for header in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{escape(str(cell))}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{thead}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


class ReportGenerator:
    """Generate HTML, JSON, and optional PDF reports from stored crawl data."""

    def __init__(self, db: DeepReconDB | None = None, reports_path: str | Path = REPORTS_PATH) -> None:
        self.db = db or DeepReconDB()
        self.reports_path = Path(reports_path)
        self.reports_path.mkdir(parents=True, exist_ok=True)

    def generate_session_report(self, session_id: int, title: str | None = None) -> dict[str, Path]:
        """Generate a session report from stored database records."""

        pages = self.db.list_pages(session_id)
        links = self.db.list_links()
        keyword_hits = self.db.list_keyword_hits(session_id)
        session = self.db.get_session(session_id)
        payload = self._build_payload(session=session, pages=pages, links=links, keyword_hits=keyword_hits)
        report_title = title or (session["name"] if session else f"Session {session_id}")
        return self._write_outputs(report_title, payload, session_id=session_id)

    def generate_legacy_report(self, data: list[dict[str, Any]], title: str = "DeepRecon Report") -> dict[str, Path]:
        """Generate a report from the legacy list-of-dicts format."""

        payload = self._build_legacy_payload(data)
        return self._write_outputs(title, payload)

    def _build_payload(
        self,
        *,
        session: dict[str, Any] | None,
        pages: list[dict[str, Any]],
        links: list[dict[str, Any]],
        keyword_hits: list[dict[str, Any]],
    ) -> dict[str, Any]:
        email_hits = sorted({email for page in pages for email in (page.get("meta", {}) or {}).get("emails", [])})
        crypto_hits = {
            "bitcoin": sorted({item for page in pages for item in (page.get("meta", {}) or {}).get("btc", [])}),
            "ethereum": sorted({item for page in pages for item in (page.get("meta", {}) or {}).get("eth", [])}),
            "monero": sorted({item for page in pages for item in (page.get("meta", {}) or {}).get("xmr", [])}),
        }
        return {
            "session": session,
            "pages": pages,
            "links": links,
            "keyword_hits": keyword_hits,
            "emails": email_hits,
            "crypto_hits": crypto_hits,
            "summary": {
                "pages_crawled": len(pages),
                "links_found": len(links),
                "keyword_hits": len(keyword_hits),
                "emails_found": len(email_hits),
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "disclaimer": DISCLAIMER,
        }

    def _build_legacy_payload(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        pages = []
        for item in data:
            pages.append(
                {
                    "url": item.get("url"),
                    "title": item.get("title"),
                    "meta": {
                        "emails": item.get("emails", []),
                        "btc": item.get("btc", []),
                        "pgp": item.get("pgp", []),
                    },
                }
            )
        return self._build_payload(session=None, pages=pages, links=[], keyword_hits=[])

    def _write_outputs(self, title: str, payload: dict[str, Any], session_id: int | None = None) -> dict[str, Path]:
        slug = title.lower().replace(" ", "_")[:50]
        timestamp = _timestamp()
        html_path = self.reports_path / f"{slug}_{timestamp}.html"
        json_path = self.reports_path / f"{slug}_{timestamp}.json"

        html_path.write_text(self._render_html(title, payload), encoding="utf-8")
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

        pdf_path: Path | None = None
        if ENABLE_PDF_EXPORT and HTML is not None:
            pdf_path = self.reports_path / f"{slug}_{timestamp}.pdf"
            HTML(string=html_path.read_text(encoding="utf-8"), base_url=str(self.reports_path)).write_pdf(pdf_path)

        if session_id is not None:
            self.db.add_report(
                {
                    "session_id": session_id,
                    "title": title,
                    "format": "html",
                    "path": str(html_path),
                    "summary": json.dumps(payload["summary"], ensure_ascii=True),
                }
            )

        LOGGER.info("Report written to %s", html_path)
        result = {"html": html_path, "json": json_path}
        if pdf_path is not None:
            result["pdf"] = pdf_path
        return result

    def _render_html(self, title: str, payload: dict[str, Any]) -> str:
        summary = payload["summary"]
        session_block = ""
        if payload.get("session"):
            session = payload["session"]
            session_block = f"<p><strong>Session:</strong> {escape(str(session.get('name', '')))}</p>"

        keyword_rows = [
            [hit.get("keyword"), hit.get("match_text"), hit.get("context", ""), hit.get("created_at", "")]
            for hit in payload.get("keyword_hits", [])
        ]
        link_rows = [
            [link.get("source_url"), link.get("target_url"), link.get("is_internal"), link.get("created_at", "")]
            for link in payload.get("links", [])
        ]
        email_items = "".join(f"<li>{escape(email)}</li>" for email in payload.get("emails", [])) or "<li>None</li>"

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; background: #f4f4f1; color: #1c1c1c; }}
    header {{ background: linear-gradient(135deg, #0f172a, #1f2937); color: white; padding: 32px; }}
    main {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
    .card {{ background: white; border: 1px solid #ddd; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.04); }}
    .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
    .summary div {{ background: #f8fafc; border-radius: 10px; padding: 16px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #e5e7eb; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #f8fafc; }}
    .disclaimer {{ background: #fff7ed; border-left: 4px solid #f59e0b; padding: 12px 16px; }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(title)}</h1>
    <p>{escape(payload.get('generated_at', ''))}</p>
  </header>
  <main>
    <div class="card disclaimer">{escape(payload.get('disclaimer', DISCLAIMER))}</div>
    <div class="card">{session_block}<div class="summary"><div><strong>Pages</strong><br>{summary['pages_crawled']}</div><div><strong>Links</strong><br>{summary['links_found']}</div><div><strong>Keywords</strong><br>{summary['keyword_hits']}</div><div><strong>Emails</strong><br>{summary['emails_found']}</div></div></div>
    <div class="card"><h2>Keyword Hits</h2>{_render_table(['Keyword', 'Match', 'Context', 'Timestamp'], keyword_rows) if keyword_rows else '<p>No keyword hits recorded.</p>'}</div>
    <div class="card"><h2>Links</h2>{_render_table(['Source', 'Target', 'Internal', 'Timestamp'], link_rows) if link_rows else '<p>No links recorded.</p>'}</div>
    <div class="card"><h2>Emails</h2><ul>{email_items}</ul></div>
  </main>
</body>
</html>"""


def save_report(data: list[dict[str, Any]]) -> dict[str, Path]:
    """Legacy helper preserved for the old CLI."""

    generator = ReportGenerator()
    return generator.generate_legacy_report(data)
