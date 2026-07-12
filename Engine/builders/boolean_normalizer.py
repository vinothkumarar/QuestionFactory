"""
Question Factory OS
Boolean Normalizer

Milestone : M12
Sprint    : S3
Release   : R1

Normalizes AI generated boolean values.
"""


class BooleanNormalizer:

    BOOLEAN_FIELDS = [

        "pyq_inspired",

        "image_required",

        "has_diagram",

        "latex_required"

    ]

    TRUE_VALUES = {

        True,

        "true",

        "True",

        "TRUE",

        "yes",

        "Yes",

        "YES",

        "y",

        "Y",

        "1",

        1

    }

    FALSE_VALUES = {

        False,

        "false",

        "False",

        "FALSE",

        "no",

        "No",

        "NO",

        "n",

        "N",

        "0",

        0,

        None,

        ""

    }

    def normalize(
        self,
        question: dict
    ) -> dict:

        for field in self.BOOLEAN_FIELDS:

            value = question.get(field)

            if value in self.TRUE_VALUES:

                question[field] = True

            elif value in self.FALSE_VALUES:

                question[field] = False

            else:

                #
                # Unknown value
                # Keep False for safety.
                #

                question[field] = False

        return question
        