"""
Question Factory OS
Logging Module

Purpose:
Centralized logging for the Automation Engine.
"""

import logging
from pathlib import Path

from config import LOG_DIR


LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "generation.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_logger():
    return logging.getLogger("QuestionFactory")
