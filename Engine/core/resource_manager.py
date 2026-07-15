"""
Question Factory Engine
Resource Manager

Purpose:
Manage the QuestionBank folder structure.
"""

from pathlib import Path
from config import QUESTIONBANK_DIR


class ResourceManager:
    """
    Handles creation and verification of QuestionBank folders.
    """

    def ensure_questionbank_path(
        self,
        project: str,
        chapter: str,
        subtopic: str,
    ) -> Path:

        folder = QUESTIONBANK_DIR / project / chapter / subtopic

        folder.mkdir(parents=True, exist_ok=True)

        return folder
