"""
Question Factory OS
State Manager

Purpose:
Read and write runtime state files.

Authoritative runtime files:

- progress.json
- metadata.json
- batch_manifest.json
"""

import json
from pathlib import Path

from Engine.config import PROGRESS_FILE, METADATA_FILE, MANIFEST_FILE

# --------------------------------------------------
# Generic Helpers
# --------------------------------------------------


def load_json(file_path: Path):
    """Load JSON from file."""

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file_path: Path, data):
    """Save JSON to file."""

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# --------------------------------------------------
# Progress
# --------------------------------------------------


def load_progress():
    return load_json(PROGRESS_FILE)


def save_progress(data):
    save_json(PROGRESS_FILE, data)


# --------------------------------------------------
# Metadata
# --------------------------------------------------


def load_metadata():
    return load_json(METADATA_FILE)


def save_metadata(data):
    save_json(METADATA_FILE, data)


# --------------------------------------------------
# Batch Manifest
# --------------------------------------------------


def load_manifest():
    return load_json(MANIFEST_FILE)


def save_manifest(data):
    save_json(MANIFEST_FILE, data)
