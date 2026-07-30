"""
Question Factory OS v2.4
Factory State Mapper

Milestone : M14
Sprint    : S3
Release   : R1
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)
from Engine.models.factory_state_model import (
    FactoryStateModel,
)


class FactoryStateMapper:
    """
    Converts a ManufacturingWorkItemModel
    into a FactoryStateModel.
    """

    @staticmethod
    def map(
        work_item: ManufacturingWorkItemModel,
    ) -> FactoryStateModel:

        return FactoryStateModel(
            subject=work_item.subject,
            unit=work_item.unit,
            chapter=work_item.chapter,
            subtopic=work_item.subtopic,
            set_no=work_item.set_no,
            current_batch=work_item.batch_no,
            questions_per_batch=work_item.questions_per_batch,
            status="RUNNING",
        )