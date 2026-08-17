"""Interactive and automated entry point for DeepRecon."""

from __future__ import annotations

import argparse
import sys

from rich.console import Console

from config import DB_PATH
from core.wizard import ReconWizard
from storage.db import DeepReconDB
from utils.banner import banner
from utils.logger import configure_logging
from utils.tor_manager import TorManager

console = Console()


def main() -> None:
    """Entry point for DeepRecon CLI, Guided Wizard, or Web UI."""
    parser = argparse.ArgumentParser(
        description="🕵️ DeepRecon - Autonomous Dark Web Reconnaissance & AI Threat Triage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  deeprecon                      # Launch Interactive Guided Wizard (Default)
  deeprecon --web                # Launch Cyber Command Web UI Dashboard
  deeprecon --web --port 8080    # Launch Web UI on custom port
  deeprecon --wizard             # Explicit interactive wizard launch
  deeprecon --cli                # Classic menu CLI mode
        """,
    )
    parser.add_argument("--web", action="store_true", help="Launch the Web UI Dashboard")
    parser.add_argument("--wizard", "--interactive", "-i", action="store_true", help="Launch the Interactive Guided Wizard (default)")
    parser.add_argument("--cli", action="store_true", help="Launch classic menu CLI mode")
    parser.add_argument("--host", default="127.0.0.1", help="Host address for Web UI (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port for Web UI (default: 8000)")

    args = parser.parse_args()
    configure_logging()

    if args.web:
        console.print(f"\n[bold green]🚀 Launching DeepRecon Cyber Command Web UI at http://{args.host}:{args.port}[/bold green]")
        console.print("[dim]Press Ctrl+C to stop server[/dim]\n")
        import uvicorn
        uvicorn.run("web.app:app", host=args.host, port=args.port, reload=False)
        return

    db = DeepReconDB(DB_PATH)
    wizard = ReconWizard(db=db)

    # Default to Interactive Guided Wizard
    wizard.run()


if __name__ == "__main__":
    main()
