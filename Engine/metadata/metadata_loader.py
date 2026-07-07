"""
Question Factory OS
Metadata Loader

Loads metadata required by the Question Builder.
"""


class MetadataLoader:

    def __init__(self):

        self.metadata = {
            "P1_CH1_ST4": {
                "subject_name": "Physics",
                "unit_name": "Units and Measurements",
                "chapter_name": "Units and Measurements",
                "subtopic_name": "Errors in Measurement"
            }
        }

    def load(self):

        return self.metadata

    def get_metadata(self, key: str):

        return self.metadata.get(key)
        