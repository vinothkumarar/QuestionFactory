"""
Question Factory OS
Execution Pipeline Builder

Milestone : M5
Sprint    : S1
Release   : R1
"""

from Engine.pipeline.execution_pipeline import (
    ExecutionPipeline,
)

from Engine.pipeline.processors.build_processor import (
    BuildProcessor,
)

from Engine.pipeline.processors.prompt_processor import (
    PromptProcessor,
)

from Engine.pipeline.processors.ai_processor import (
    AIProcessor,
)

from Engine.pipeline.processors.parse_processor import (
    ParseProcessor,
)

from Engine.pipeline.processors.merge_processor import (
    MergeProcessor,
)

from Engine.pipeline.processors.validation_processor import (
    ValidationProcessor,
)


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
