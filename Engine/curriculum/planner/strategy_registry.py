"""
Question Factory OS v2.4
Manufacturing Strategy Registry

Milestone : M14
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

from typing import Dict

from Engine.curriculum.manufacturing_scope import (
    ManufacturingScope,
)
from Engine.curriculum.planner.base_strategy import (
    BaseManufacturingStrategy,
)
from Engine.curriculum.planner.strategies.one_batch_strategy import (
    OneBatchStrategy,
)

from Engine.curriculum.planner.strategies.subtopic_strategy import (
    SubtopicStrategy,
)

from Engine.curriculum.planner.strategies.chapter_strategy import (
    ChapterStrategy,
)

from Engine.curriculum.repositories.in_memory_curriculum_repository import (
    InMemoryCurriculumRepository,
)

from Engine.curriculum.planner.strategies.unit_strategy import (
    UnitStrategy,
)

from Engine.curriculum.planner.strategies.subject_strategy import (
    SubjectStrategy,
)

class StrategyRegistry:
    """
    Registry for curriculum manufacturing strategies.

    Maps a ManufacturingScope to its corresponding
    strategy implementation.
    """

    def __init__(self) -> None:

        self._strategies: Dict[
            ManufacturingScope,
            BaseManufacturingStrategy,
        ] = {}

        self._register_defaults()

    def _register_defaults(self) -> None:

        repository = InMemoryCurriculumRepository()

        self.register(
            ManufacturingScope.ONE_BATCH,
            OneBatchStrategy(),
        )

        self.register(
            ManufacturingScope.SUBTOPIC,
            SubtopicStrategy(),
        )

        self.register(
            ManufacturingScope.CHAPTER,
            ChapterStrategy(repository),
        )

        self.register(
            ManufacturingScope.UNIT,
            UnitStrategy(repository),
        )

        self.register(
            ManufacturingScope.SUBJECT,
            SubjectStrategy(repository),
        )

    def register(
        self,
        scope: ManufacturingScope,
        strategy: BaseManufacturingStrategy,
    ) -> None:

        self._strategies[scope] = strategy

    def get(
        self,
        scope: ManufacturingScope,
    ) -> BaseManufacturingStrategy:

        try:

            return self._strategies[scope]

        except KeyError as ex:

            raise ValueError(
                f"No strategy registered for scope '{scope}'."
            ) from ex

    def has(
        self,
        scope: ManufacturingScope,
    ) -> bool:

        return scope in self._strategies

    @property
    def registered_scopes(
        self,
    ) -> tuple[ManufacturingScope, ...]:

        return tuple(self._strategies.keys())