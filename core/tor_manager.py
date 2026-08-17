"""Tor session and circuit management compatibility layer.

Re-exports core Tor capabilities from utils.tor_manager.
"""

from __future__ import annotations

from utils.tor_manager import TorManager, TorStatus, get_session, renew_ip

__all__ = ["TorManager", "TorStatus", "get_session", "renew_ip"]
