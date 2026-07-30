"""
Question Factory OS v2.4
Factory Runtime Service

Milestone : M15
Sprint    : S1
Release   : R1

Responsible for preparing the production runtime
before FactoryRunner executes.
"""

from __future__ import annotations

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)
from Engine.curriculum.mappers.factory_state_mapper import (
    FactoryStateMapper,
)
from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)


class FactoryRuntimeService:
    """
    Prepares the Question Factory runtime.

    Responsibilities
    ----------------
    • Convert WorkItem → FactoryState
    • Persist FactoryState

    Does NOT execute FactoryRunner.
    """

    def __init__(
        self,
        repository: FactoryStateRepository | None = None,
    ) -> None:

        self._repository = (
            repository
            or FactoryStateRepository()
        )

    def prepare(
        self,
        work_item: ManufacturingWorkItemModel,
    ) -> None:
        """
        Prepare runtime for a work item.
        """

        state = FactoryStateMapper.map(
            work_item
        )

        self._repository.save(
            state
        )