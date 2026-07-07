"""
Question Factory OS
Metadata Enricher

Applies metadata to a Question object.
"""

from metadata.metadata_loader import MetadataLoader


class MetadataEnricher:

    def __init__(self):
        self.metadata_loader = MetadataLoader()

    def apply(self, question: dict, runtime: dict):

        metadata_key = (
            f"{runtime['current_project']}_"
            f"{runtime['current_chapter']}_"
            f"{runtime['current_subtopic']}"
        )

        metadata = self.metadata_loader.get_metadata(metadata_key)

        if metadata:
            question.update(metadata)

        return question
        