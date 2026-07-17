"""
Question Factory OS
Generation Status Test
"""

from Engine.constants.generation_status import GenerationStatus

print("=" * 80)
print("GENERATION STATUS")
print("=" * 80)

print("SUCCESS            :", GenerationStatus.SUCCESS)
print("FAILED             :", GenerationStatus.FAILED)
print("AI_FAILED          :", GenerationStatus.AI_FAILED)
print("PARSE_FAILED       :", GenerationStatus.PARSE_FAILED)
print("VALIDATION_FAILED  :", GenerationStatus.VALIDATION_FAILED)
print("EXPORT_FAILED      :", GenerationStatus.EXPORT_FAILED)
print("RETRY              :", GenerationStatus.RETRY)
print("SKIPPED            :", GenerationStatus.SKIPPED)
