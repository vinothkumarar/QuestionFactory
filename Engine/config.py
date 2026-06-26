"""
Question Factory OS
Configuration Module

Purpose:
Centralize all project paths and global constants.
"""

from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------

# Engine/
ENGINE_DIR = Path(__file__).resolve().parent

# QuestionFactory/
PROJECT_ROOT = ENGINE_DIR.parent

# --------------------------------------------------
# BLUEPRINT
# --------------------------------------------------

BLUEPRINT_DIR = PROJECT_ROOT / "Blueprint"

# --------------------------------------------------
# RUNTIME STATE
# --------------------------------------------------

PROGRESS_DIR = PROJECT_ROOT / "Progress"
METADATA_DIR = PROJECT_ROOT / "Metadata"
MANIFEST_DIR = PROJECT_ROOT / "BatchManifest"

PROGRESS_FILE = PROGRESS_DIR / "progress.json"
METADATA_FILE = METADATA_DIR / "metadata.json"
MANIFEST_FILE = MANIFEST_DIR / "batch_manifest.json"

# --------------------------------------------------
# QUESTION STORAGE
# --------------------------------------------------

QUESTIONBANK_DIR = PROJECT_ROOT / "QuestionBank"

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

UPLOAD_DIR = PROJECT_ROOT / "Upload"
ERROR_DIR = PROJECT_ROOT / "ErrorRepair"

# --------------------------------------------------
# LOGS
# --------------------------------------------------

LOG_DIR = PROJECT_ROOT / "Logs"

# --------------------------------------------------
# VERSION
# --------------------------------------------------

FACTORY_VERSION = "1.3"

FACTORY_NAME = "Question Factory OS"
