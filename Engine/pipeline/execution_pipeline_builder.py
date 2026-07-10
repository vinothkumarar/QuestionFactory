"""
Question Factory OS
Execution Pipeline Builder

Milestone : M5
Sprint    : S1
Release   : R1
"""

from pipeline.execution_pipeline import ExecutionPipeline

from pipeline.processors.build_processor import BuildProcessor
from pipeline.processors.prompt_processor import PromptProcessor
from pipeline.processors.ai_processor import AIProcessor
from pipeline.processors.parse_processor import ParseProcessor
from pipeline.processors.merge_processor import MergeProcessor
from pipeline.processors.validation_processor import ValidationProcessor


class ExecutionPipelineBuilder:
    """
    Builds the default production pipeline.
    """

    def build(self) -> ExecutionPipeline:

        pipeline = ExecutionPipeline()

        pipeline.add_processor(BuildProcessor())

        pipeline.add_processor(PromptProcessor())

        pipeline.add_processor(AIProcessor())

        pipeline.add_processor(ParseProcessor())

        pipeline.add_processor(MergeProcessor())

        pipeline.add_processor(ValidationProcessor())

        return pipeline
        