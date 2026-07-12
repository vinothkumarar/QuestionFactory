"""
Question Factory OS
Required Field Validator

Milestone : M12
Sprint    : S4
Release   : R1

Validates mandatory educational fields and
basic question quality.
"""

from core.schema import QUESTION_REQUIRED_FIELDS


class RequiredFieldValidator:

    MIN_QUESTION_LENGTH = 25

    MIN_EXPLANATION_LENGTH = 40

    OPTION_FIELDS = [

        "option_a",
        "option_b",
        "option_c",
        "option_d"

    ]

    def validate(
        self,
        question: dict
    ):

        errors = []

        #
        # Required Fields
        #

        for field in QUESTION_REQUIRED_FIELDS:

            value = question.get(field)

            if value is None:

                errors.append(
                    f"{field} is required"
                )

            elif isinstance(value, str):

                if value.strip() == "":

                    errors.append(
                        f"{field} is required"
                    )

        #
        # Question Length
        #

        question_text = question.get(
            "question_text",
            ""
        )

        if len(question_text.strip()) < self.MIN_QUESTION_LENGTH:

            errors.append(
                "Question text is too short."
            )

        #
        # Explanation Length
        #

        explanation = question.get(
            "explanation",
            ""
        )

        if len(explanation.strip()) < self.MIN_EXPLANATION_LENGTH:

            errors.append(
                "Explanation is too short."
            )

        #
        # Concept Tested
        #

        concept = question.get(
            "concept_tested",
            ""
        )

        if concept.strip() == "":

            errors.append(
                "concept_tested is empty."
            )

        #
        # Correct Option
        #

        correct = question.get(
            "correct_option"
        )

        if correct not in {

            "A",
            "B",
            "C",
            "D"

        }:

            errors.append(
                "Invalid correct_option."
            )

        #
        # Duplicate Options
        #

        options = []

        for field in self.OPTION_FIELDS:

            option = question.get(
                field,
                ""
            ).strip()

            options.append(option)

        if len(set(options)) != 4:

            errors.append(
                "Duplicate answer options detected."
            )

        return {

            "validator":
                "RequiredFieldValidator",

            "passed":
                len(errors) == 0,

            "errors":
                errors

        }
        