"""
Question Factory OS
Metadata Loader

Milestone : M12
Sprint    : S1
Release   : R1

Loads production metadata used by the
Question Builder.
"""


class MetadataLoader:

    def __init__(self):

        self.metadata = {

            "P1_CH1_ST4": {

                #
                # Database IDs
                #

                "subject_id": "PHY",

                "unit_id": "P1",

                "chapter_id": "CH1",

                "subtopic_id": "ST4",

                #
                # Display Names
                #

                "subject_name": "Physics",

                "unit_name": "Units and Measurements",

                "chapter_name": "Units and Measurements",

                "subtopic_name": "Errors in Measurement",

                #
                # Factory Defaults
                #

                "language": "English",

                "marks": 4,

                "negative_marks": -1,

                "status": "Draft",

                "version": "1.0"

            }

        }

    def load(self):

        return self.metadata

    def get_metadata(
        self,
        key: str
    ):

        return self.metadata.get(key)
        