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
except (ImportError, OSError, Exception):  # pragma: no cover - optional dependency
    HTML = None


from config import ENABLE_PDF_EXPORT, REPORTS_PATH
from core.parser import PageData
from storage.db import DeepReconDB
from utils.logger import get_logger


LOGGER = get_logger(__name__)
DISCLAIMER = (
    "Ethical use only: DeepRecon is intended for authorized security research, "
    "threat intelligence, and defensive OSINT investigations."
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
            "bitcoin": sorted({
                item for page in pages
                for item in (
                    (page.get("meta", {}) or {}).get("crypto_addresses")
                    or (page.get("meta", {}) or {}).get("crypto")
                    or {}
                ).get("bitcoin", (page.get("meta", {}) or {}).get("btc", []))
            }),
            "ethereum": sorted({
                item for page in pages
                for item in (
                    (page.get("meta", {}) or {}).get("crypto_addresses")
                    or (page.get("meta", {}) or {}).get("crypto")
                    or {}
                ).get("ethereum", (page.get("meta", {}) or {}).get("eth", []))
            }),
            "monero": sorted({
                item for page in pages
                for item in (
                    (page.get("meta", {}) or {}).get("crypto_addresses")
                    or (page.get("meta", {}) or {}).get("crypto")
                    or {}
                ).get("monero", (page.get("meta", {}) or {}).get("xmr", []))
            }),
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
                "btc_found": len(crypto_hits["bitcoin"]),
                "eth_found": len(crypto_hits["ethereum"]),
                "xmr_found": len(crypto_hits["monero"]),
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
            session_block = f"<p class='session-meta'><strong>Session:</strong> {escape(str(session.get('name', '')))} &nbsp;|&nbsp; <strong>Target:</strong> {escape(str(session.get('seed_url', '')))}</p>"

        keyword_rows = [
            [hit.get("keyword"), hit.get("match_text"), hit.get("context", ""), hit.get("created_at", "")]
            for hit in payload.get("keyword_hits", [])
        ]
        link_rows = [
            [link.get("source_url"), link.get("target_url"), link.get("is_internal"), link.get("created_at", "")]
            for link in payload.get("links", [])
        ]
        
        email_items = "".join(f"<span class='tag email-tag'>{escape(email)}</span>" for email in payload.get("emails", [])) or "<p class='empty-state'>No email addresses detected.</p>"
        
        crypto_hits = payload.get("crypto_hits", {})
        btc_items = "".join(f"<span class='tag btc-tag'>BTC: {escape(addr)}</span>" for addr in crypto_hits.get("bitcoin", []))
        eth_items = "".join(f"<span class='tag eth-tag'>ETH: {escape(addr)}</span>" for addr in crypto_hits.get("ethereum", []))
        xmr_items = "".join(f"<span class='tag xmr-tag'>XMR: {escape(addr)}</span>" for addr in crypto_hits.get("monero", []))
        all_crypto = btc_items + eth_items + xmr_items or "<p class='empty-state'>No cryptocurrency addresses detected.</p>"

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DeepRecon OSINT Report - {escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-primary: #0a0e17;
      --bg-card: #111827;
      --bg-card-hover: #1f2937;
      --accent-cyan: #00f2fe;
      --accent-blue: #4facfe;
      --accent-purple: #9d4edd;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
      --border-color: #334155;
      --alert-bg: rgba(245, 158, 11, 0.1);
      --alert-border: #f59e0b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-primary);
      color: var(--text-main);
      padding: 0;
      line-height: 1.6;
    }}
    header {{
      background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #0f172a 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 40px 32px;
    }}
    .header-content {{ max-width: 1280px; margin: 0 auto; }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: rgba(0, 242, 254, 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(0, 242, 254, 0.4);
      margin-bottom: 12px;
    }}
    h1 {{ font-size: 2.25rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; margin-bottom: 8px; }}
    .timestamp {{ font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: var(--text-muted); }}
    main {{ max-width: 1280px; margin: 0 auto; padding: 32px 24px; }}
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }}
    .card h2 {{ font-size: 1.25rem; font-weight: 600; color: #fff; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }}
    .session-meta {{ color: var(--text-muted); margin-bottom: 16px; font-size: 0.95rem; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 16px;
    }}
    .stat-box {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
    }}
    .stat-number {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.75rem;
      font-weight: 700;
      color: var(--accent-cyan);
      margin-top: 4px;
    }}
    .stat-label {{ font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; }}
    .tag-container {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .tag {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid transparent;
    }}
    .email-tag {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }}
    .btc-tag {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }}
    .eth-tag {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; border-color: rgba(168, 85, 247, 0.3); }}
    .xmr-tag {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border-color: rgba(239, 68, 68, 0.3); }}
    .table-responsive {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
    th, td {{ border-bottom: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: top; }}
    th {{ background: #0f172a; color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }}
    tr:hover {{ background: rgba(255, 255, 255, 0.02); }}
    .disclaimer {{ background: var(--alert-bg); border-left: 4px solid var(--alert-border); padding: 16px; font-size: 0.9rem; color: #fef3c7; }}
    .empty-state {{ color: var(--text-muted); font-style: italic; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <header>
    <div class="header-content">
      <span class="badge">DeepRecon OSINT Framework</span>
      <h1>{escape(title)}</h1>
      <p class="timestamp">Generated at: {escape(payload.get('generated_at', ''))}</p>
    </div>
  </header>
  <main>
    <div class="card disclaimer">
      ⚠️ <strong>Legal & Ethical Notice:</strong> {escape(payload.get('disclaimer', DISCLAIMER))}
    </div>

    <div class="card">
      <h2>📊 Investigation Overview</h2>
      {session_block}
      <div class="summary-grid">
        <div class="stat-box"><div class="stat-label">Pages Crawled</div><div class="stat-number">{summary.get('pages_crawled', 0)}</div></div>
        <div class="stat-box"><div class="stat-label">Links Found</div><div class="stat-number">{summary.get('links_found', 0)}</div></div>
        <div class="stat-box"><div class="stat-label">Keyword Hits</div><div class="stat-number">{summary.get('keyword_hits', 0)}</div></div>
        <div class="stat-box"><div class="stat-label">Emails Extracted</div><div class="stat-number">{summary.get('emails_found', 0)}</div></div>
        <div class="stat-box"><div class="stat-label">Crypto Wallets</div><div class="stat-number">{summary.get('btc_found', 0) + summary.get('eth_found', 0) + summary.get('xmr_found', 0)}</div></div>
      </div>
    </div>

    <div class="card">
      <h2>💰 Cryptocurrency Intelligence</h2>
      <div class="tag-container">{all_crypto}</div>
    </div>

    <div class="card">
      <h2>📧 Discovered Emails</h2>
      <div class="tag-container">{email_items}</div>
    </div>

    <div class="card">
      <h2>🎯 Keyword & Pattern Matches</h2>
      <div class="table-responsive">
        {_render_table(['Keyword', 'Match', 'Context', 'Timestamp'], keyword_rows) if keyword_rows else '<p class="empty-state">No keyword hits recorded.</p>'}
      </div>
    </div>

    <div class="card">
      <h2>🔗 Discovered Traversal Links</h2>
      <div class="table-responsive">
        {_render_table(['Source', 'Target', 'Internal', 'Timestamp'], link_rows) if link_rows else '<p class="empty-state">No links recorded.</p>'}
      </div>
    </div>
  </main>
</body>
</html>"""


def save_report(data: list[dict[str, Any]]) -> dict[str, Path]:
    """Legacy helper preserved for backwards compatibility."""

    generator = ReportGenerator()
    return generator.generate_legacy_report(data)
