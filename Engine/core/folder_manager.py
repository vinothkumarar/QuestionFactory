"""
Question Factory OS
Folder Manager
"""

from pathlib import Path


class FolderManager:

    def create_output_folder(self, question: dict) -> Path:

        subject = self._safe_name(question["subject_name"])

        unit = self._safe_name(question["unit_name"])

        chapter = self._safe_name(question["chapter_name"])

        subtopic = self._safe_name(question["subtopic_name"])

        folder = (
            Path("output")
            / subject
            / f'{question["project_code"]}_{unit}'
            / f'{question["chapter_code"]}_{chapter}'
            / f'{question["subtopic_code"]}_{subtopic}'
        )

        folder.mkdir(parents=True, exist_ok=True)

        return folder

    def _safe_name(self, text: str) -> str:

        return (
            text.strip()
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "-")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
            .replace(" ", "_")
        )
