"""
Question Factory OS
Pipeline Status Test

Version : 2.3.7.1.3
"""

from constants.pipeline_status import PipelineStatus


print("=" * 80)
print("PIPELINE STATUS")
print("=" * 80)

print("PLANNED     :", PipelineStatus.PLANNED)
print("BUILDING    :", PipelineStatus.BUILDING)
print("PROMPTING   :", PipelineStatus.PROMPTING)
print("GENERATING  :", PipelineStatus.GENERATING)
print("PARSING     :", PipelineStatus.PARSING)
print("MERGING     :", PipelineStatus.MERGING)
print("VALIDATING  :", PipelineStatus.VALIDATING)
print("EXPORTING   :", PipelineStatus.EXPORTING)
print("COMPLETED   :", PipelineStatus.COMPLETED)
print("FAILED      :", PipelineStatus.FAILED)
