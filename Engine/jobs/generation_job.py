"""
Question Factory OS
Generation Job
"""


class GenerationJob:

    def __init__(
        self,
        runtime: dict,
        start_question: int,
        count: int
    ):

        self.runtime = runtime

        self.start_question = start_question

        self.count = count
        