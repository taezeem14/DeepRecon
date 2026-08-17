"""Visual ASCII art banner and branding for DeepRecon."""

from __future__ import annotations

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

try:
    from colorama import Fore, Style
    _HAS_COLORAMA = True
except ImportError:
    _HAS_COLORAMA = False

BANNER_TEXT = r"""
██████╗ ███████╗███████╗██████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝█████╗  ██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══██╗██╔══╝  ██║   ██║██║╚██╗██║
██████╔╝███████╗███████╗██║     ██║  ██║███████╗╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
"""


def banner(version: str = "v3.2.0") -> None:
    """Print high-contrast DeepRecon cyber banner."""
    if _HAS_RICH:
        console = Console()
        text = Text(BANNER_TEXT, style="bold cyan")
        console.print(text)
        console.print(f"[bold magenta]⚡ Autonomous Dark Web OSINT & Intelligence Framework[/bold magenta] [dim]({version})[/dim]\n")
    elif _HAS_COLORAMA:
        print(Fore.CYAN + BANNER_TEXT + Style.RESET_ALL)
        print(Fore.MAGENTA + f"⚡ Autonomous Dark Web OSINT & Intelligence Framework ({version})\n" + Style.RESET_ALL)
    else:
        print(BANNER_TEXT)
        print(f"Autonomous Dark Web OSINT & Intelligence Framework ({version})\n")
