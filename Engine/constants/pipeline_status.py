"""
Question Factory OS
Pipeline Status

Version : 2.3.7.1.3
"""


class PipelineStatus:

    # -------------------------------------------------
    # Initial State
    # -------------------------------------------------

    PLANNED = "PLANNED"

    # -------------------------------------------------
    # Execution Stages
    # -------------------------------------------------

    BUILDING = "BUILDING"

    PROMPTING = "PROMPTING"

    GENERATING = "GENERATING"

    PARSING = "PARSING"

    MERGING = "MERGING"

    VALIDATING = "VALIDATING"

    EXPORTING = "EXPORTING"

    # -------------------------------------------------
    # Final States
    # -------------------------------------------------

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"
    