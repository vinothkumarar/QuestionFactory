"""
Question Factory OS
Runtime Manager

Purpose:
Manage runtime state transitions for the Question Factory.
"""

from core.state_manager import (
    load_progress,
    save_progress,
    load_metadata,
    save_metadata,
    load_manifest,
    save_manifest,
)


class RuntimeManager:

    def __init__(self):
        self.progress = load_progress()
        self.metadata = load_metadata()
        self.manifest = load_manifest()

    # -----------------------------------------
    # Get Current Runtime
    # -----------------------------------------

    def get_current_node(self):
        return self.progress.get("current_node")

    def get_current_batch(self):
        return self.progress.get("current_batch")

    def get_current_set(self):
        return self.progress.get("current_set")

    # -----------------------------------------
    # Save Runtime
    # -----------------------------------------

    def save(self):
        save_progress(self.progress)
        save_metadata(self.metadata)
        save_manifest(self.manifest)
