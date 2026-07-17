"""
Question Factory OS

Logging Module

Provides centralized logging for the
Question Factory Automation Engine.
"""

from __future__ import annotations

import logging

from Engine.config import LOG_DIR


#
# Ensure log directory exists
#

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIR / "generation.log"


#
# Configure root logging
#

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def get_logger() -> logging.Logger:
    """
    Return the shared Question Factory logger.
    """

    return logging.getLogger("QuestionFactory")