"""
Question Factory OS v2.4
SUBTOPIC Manufacturing Strategy

Milestone : M16
Sprint    : S1
Release   : R1
"""

from __future__ import annotations

import uuid

from Engine.curriculum.manufacturing_queue import (
    ManufacturingQueue,
)
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)
from Engine.curriculum.planner.base_strategy import (
    BaseManufacturingStrategy,
)

from Engine.catalog.archetype_catalog.archetype_catalog_loader import (
    ArchetypeCatalogLoader,
)

class SubtopicStrategy(BaseManufacturingStrategy):
    """
    Expands a SUBTOPIC request into one
    ManufacturingWorkItem per batch.
    """

    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:

        request.validate()

        queue = ManufacturingQueue()

        archetype_loader = ArchetypeCatalogLoader()

        archetypes = archetype_loader.load(
            request.subtopic,
        )

        for set_no in range(
            int(request.start_set[1:]),
            int(request.end_set[1:]) + 1,
        ):

            for archetype in archetypes:

                work_item = ManufacturingWorkItemModel(
                    request_id=request.request_id,
                    work_item_id=(
                        f"WI_{uuid.uuid4().hex[:8].upper()}"
                    ),
                    subject=request.subject,
                    unit=request.unit,
                    chapter=request.chapter,
                    subtopic=request.subtopic,
                    set_no=f"S{set_no}",
                    batch_no=1,
                    questions_per_batch=(
                        request.questions_per_batch
                    ),
                    question_start=1,
                    question_end=(
                        request.questions_per_batch
                    ),
                    concept_id=archetype["concept_id"],
                    concept=archetype["concept"],
                    qp_id=archetype["qp_id"],
                    question_possibility=(
                        archetype["question_possibility"]
                    ),
                    archetype_id=archetype["archetype_id"],
                    archetype=archetype["archetype"],
                    variation_capacity=archetype.get(
                        "variation_capacity",
                        "",
                    ),
                    variation_dimensions=archetype.get(
                        "variation_dimensions",
                        [],
                    ),
                )

                queue.enqueue(work_item)

        return queue