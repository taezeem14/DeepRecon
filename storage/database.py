"""Backward-compatible import wrapper for the legacy storage module."""

from storage.db import DeepReconDB, init_db, save_result

__all__ = ["DeepReconDB", "init_db", "save_result"]
