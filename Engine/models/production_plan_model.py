"""
Question Factory OS
Production Plan Model

Milestone : M13
Sprint    : S2
Release   : R1
"""

from dataclasses import dataclass


@dataclass
class ProductionPlanModel:

    project: str

    chapter: str

    subtopic: str

    set_no: str

    start_batch: int

    end_batch: int

    questions_per_batch: int = 100

    auto_commit: bool = True

    stop_on_failure: bool = True
