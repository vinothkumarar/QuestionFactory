"""
Question Factory OS
File Name Generator
"""


class FileNameGenerator:

    def generate(
        self,
        runtime: dict
    ) -> str:

        project = runtime["current_project"]

        chapter = runtime["current_chapter"]

        subtopic = runtime["current_subtopic"]

        set_no = runtime["current_set"]

        batch = runtime.get(
            "current_batch",
            1
        )

        return (
            f"{project}_"
            f"{chapter}_"
            f"{subtopic}_"
            f"{set_no}_"
            f"B{batch}.csv"
        )
        