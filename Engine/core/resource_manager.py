"""
Question Factory OS
Resource Manager

Purpose:
Ensure the required folder structure exists for the current node.
"""

from pathlib import Path

from config import QUESTIONBANK_DIR


def ensure_questionbank_path(project, chapter, subtopic):
    """
    Create QuestionBank folder hierarchy if it does not exist.

    Returns:
        Path object of the subtopic folder.
    """

    path = (
        QUESTIONBANK_DIR
        / project
        / chapter
        / subtopic
    )

    path.mkdir(parents=True, exist_ok=True)

    return path
