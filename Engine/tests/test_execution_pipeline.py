"""
Question Factory OS
Execution Pipeline Test
"""

from Engine.pipeline.execution_pipeline import ExecutionPipeline


class DummyStage:

    def execute(self, context):

        context.append("Executed")

        return context


pipeline = ExecutionPipeline()

pipeline.add_stage(DummyStage())

pipeline.add_stage(DummyStage())

pipeline.add_stage(DummyStage())


result = pipeline.run([])

print("=" * 80)
print("EXECUTION PIPELINE")
print("=" * 80)

print(result)
