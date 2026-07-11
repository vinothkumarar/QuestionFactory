"""
Question Factory OS
Production Request Model Test

Milestone : M9
Sprint    : S1
Release   : R1
"""

from models.production_request_model import (
    ProductionRequestModel
)

request = ProductionRequestModel(

    request_id="REQ_001",

    subject="Physics",

    unit="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    total_questions=250

)

print("=" * 80)
print("PRODUCTION REQUEST MODEL")
print("=" * 80)

print()

print(request)
