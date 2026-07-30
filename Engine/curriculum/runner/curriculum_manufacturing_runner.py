"""
Question Factory OS v2.5
Curriculum Manufacturing Runner

Milestone : M14
Sprint    : S3
Release   : R4
"""

from __future__ import annotations

from Engine.curriculum.execution.manufacturing_work_item_executor import (
    ManufacturingWorkItemExecutor,
)
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)
from Engine.curriculum.planner.curriculum_manufacturing_planner import (
    CurriculumManufacturingPlanner,
)


class CurriculumManufacturingRunner:
    """
    Executes curriculum manufacturing requests.

    Responsibilities
    ----------------
    1. Validate the request.
    2. Build the manufacturing queue.
    3. Iterate through the queue.
    4. Delegate each work item to the executor.

    This class intentionally contains no production logic.
    """

    VERSION = "2.5.0"

    def __init__(
        self,
        planner: CurriculumManufacturingPlanner,
        executor: ManufacturingWorkItemExecutor,
    ) -> None:
        self._planner = planner
        self._executor = executor

    def execute(
        self,
        request: ManufacturingRequestModel,
    ) -> int:
        """
        Execute a curriculum manufacturing request.

        Returns
        -------
        int
            Number of work items executed.
        """

        request.validate()

        queue = self._planner.build(request)

        processed = 0

        while queue.has_next:
            work_item = queue.dequeue()
            self._executor.execute(work_item)
            processed += 1

        return processed

    @property
    def version(self) -> str:
        return self.VERSION

    @property
    def component_name(self) -> str:
        return self.__class__.__name__

    def health(self) -> dict[str, object]:
        return {
            "component": self.component_name,
            "version": self.version,
            "status": "READY",
        }

    def diagnostics(self) -> dict[str, object]:
        return {
            "component": self.component_name,
            "version": self.version,
        }


__all__ = [
    "CurriculumManufacturingRunner",
]