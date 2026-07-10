"""
Question Factory OS
Execution Pipeline

Milestone : M4
Sprint    : S1
Release   : R1
"""

from models.pipeline_context_model import PipelineContextModel


class ExecutionPipeline:
    """
    Executes all registered processors
    sequentially.
    """

    def __init__(self):

        self.processors = []

    def add_processor(
        self,
        processor
    ):

        self.processors.append(processor)

    def clear(self):

        self.processors.clear()

    def size(self):

        return len(self.processors)

    def run(
        self,
        context: PipelineContextModel
    ) -> PipelineContextModel:

        for processor in self.processors:

            context = processor.execute(context)

        return context