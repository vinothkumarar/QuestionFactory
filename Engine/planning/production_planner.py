"""
Question Factory OS v2.2
Production Planner

Responsible for converting the current factory state into
production-ready manufacturing objects.

Responsibilities
----------------
- Load runtime state
- Resolve curriculum hierarchy
- Load blueprint metadata
- Build ProductionOrderModel
- Build ProductionNodeModel
"""

from __future__ import annotations

from typing import Any

from Engine.blueprint.blueprint_loader import (
    BlueprintLoader,
)


from Engine.models.factory_state_model import (
    FactoryStateModel,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

from Engine.planning.production_order_id_generator import (
    ProductionOrderIdGenerator,
)

from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)

from Engine.runtime.factory_state_manager import (
    FactoryStateManager,
)

from Engine.models.production_node_model import (
    ProductionNodeModel,
)

class ProductionPlanner:
    """
    Central planning component for Question Factory OS.

    This planner bridges the gap between the runtime state,
    curriculum hierarchy and blueprint configuration before
    manufacturing begins.

    Existing callers may continue using::

        planner.plan(state)

    Future manufacturing components will additionally use::

        planner.build_node(...)
        planner.build_queue(...)
    """

    def __init__(self) -> None:

        self.state_repository = FactoryStateRepository()

        self.state_manager = FactoryStateManager()

        
        self.blueprint_loader = BlueprintLoader()

        self.id_generator = ProductionOrderIdGenerator()

    # ---------------------------------------------------------
    # Private helpers
    # (implemented in Part 2)
    # ---------------------------------------------------------

    def _resolve_curriculum(
        self,
        state: FactoryStateModel,
    ) -> Any:
        ...

    def _load_blueprint(
        self,
        state: FactoryStateModel,
    ) -> Any:
        ...

    def _generate_order_id(
        self,
        state: FactoryStateModel,
    ) -> str:

        return self.id_generator.generate(state)
    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    def _question_start(
        self,
        state: FactoryStateModel,
    ) -> int:
        """
        Calculate the starting question number for the
        current production batch.
        """

        return self.state_manager.get_question_start(state)

    def _question_end(
        self,
        state: FactoryStateModel,
    ) -> int:
        """
        Calculate the ending question number for the
        current production batch.
        """

        return (
            self._question_start(state)
            + state.questions_per_batch
            - 1
        )

    
        """
        Generate a unique production order identifier.
        """

        return self.id_generator.generate(state)

    def _populate_location(
        self,
        node: ProductionNodeModel,
        state: FactoryStateModel,
    ) -> None:
        """
        Populate manufacturing location information.
        """

        node.location.subject = state.subject
        node.location.unit = state.unit
        node.location.chapter = state.chapter
        node.location.subtopic = state.subtopic

        try:
            node.location.set_number = int(
                state.set_no.replace("S", "")
            )
        except ValueError:
            node.location.set_number = 1

        node.location.batch_number = state.current_batch

    def _populate_question_range(
        self,
        node: ProductionNodeModel,
        state: FactoryStateModel,
    ) -> None:
        """
        Populate question range information.
        """

        start = self._question_start(state)

        node.question_range.question_from = start

        node.question_range.question_to = (
            start
            + state.questions_per_batch
            - 1
        )

        node.question_range.expected_questions = (
            state.questions_per_batch
        )

    def _populate_execution(
        self,
        node: ProductionNodeModel,
        state: FactoryStateModel,
    ) -> None:
        """
        Populate execution metadata.
        """

        node.execution.execution_order = (
            state.current_batch
        )

        node.execution.priority = 100

        node.execution.retry_count = 0

    def _populate_metadata(
        self,
        node: ProductionNodeModel,
        state: FactoryStateModel,
    ) -> None:
        """
        Populate production metadata.
        """

        blueprint = self.blueprint_loader.load()

        node.metadata.production_node = (
            f"{state.subject}_"
            f"{state.unit}_"
            f"{state.chapter}_"
            f"{state.subtopic}_"
            f"{state.set_no}_"
            f"B{state.current_batch}"
        )

        node.metadata.batch_id = (
            f"{state.subject}_"
            f"{state.unit}_"
            f"{state.chapter}_"
            f"{state.subtopic}_"
            f"B{state.current_batch}"
        )

        node.metadata.factory_version = (
            blueprint.factory.version
        )

        node.metadata.blueprint_version = (
            blueprint.blueprint_version
        )

        node.metadata.tags.update(
            {
                "subject": state.subject,
                "unit": state.unit,
                "chapter": state.chapter,
                "subtopic": state.subtopic,
                "set": state.set_no,
                "batch": state.current_batch,
            }
        )
    # ---------------------------------------------------------
    # Production Node Builder
    # ---------------------------------------------------------

    def build_node(
        self,
        state: FactoryStateModel,
    ) -> ProductionNodeModel:
        """
        Build the canonical manufacturing node.

        Every downstream subsystem consumes this object.

        The planner is responsible for populating all
        manufacturing metadata before execution begins.
        """

        node = ProductionNodeModel()

        # ---------------------------------------------
        # Manufacturing Location
        # ---------------------------------------------

        self._populate_location(
            node,
            state,
        )

        # ---------------------------------------------
        # Question Range
        # ---------------------------------------------

        self._populate_question_range(
            node,
            state,
        )

        # ---------------------------------------------
        # Execution
        # ---------------------------------------------

        self._populate_execution(
            node,
            state,
        )

        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        self._populate_metadata(
            node,
            state,
        )

        # ---------------------------------------------
        # Initial Production State
        # ---------------------------------------------

        node.status = "PLANNED"

        node.current_stage = "SCHEDULED"

        node.manufactured_questions = 0

        node.approved_questions = 0

        node.rejected_questions = 0

        node.repair_cycles = 0

        # ---------------------------------------------
        # Blueprint Runtime Configuration
        # ---------------------------------------------

        blueprint = self.blueprint_loader.load()

        node.execution.max_retry = (
            blueprint.runtime.max_repair_cycles
        )

        node.quality.repair_before_expand = (
            blueprint.runtime.repair_before_expand
        )

        return node
    # ---------------------------------------------------------
    # Production Order
    # ---------------------------------------------------------

    def plan(
        self,
        state: FactoryStateModel,
    ) -> ProductionOrderModel:
        """
        Build a production order from the canonical
        ProductionNodeModel.

        This method is retained for backward compatibility.
        """

        node = self.build_node(state)

        return ProductionOrderModel(
            order_id=self._generate_order_id(state),
            subject=node.location.subject,
            unit=node.location.unit,
            chapter=node.location.chapter,
            subtopic=node.location.subtopic,
            set_no=f"S{node.location.set_number}",
            batch_no=node.location.batch_number,
            question_start=node.question_range.question_from,
            question_count=node.question_range.expected_questions,
            status=node.status,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
        state: FactoryStateModel,
    ) -> dict[str, object]:
        """
        Return a concise planning summary.
        """

        node = self.build_node(state)

        return {
            "production_node": node.production_node,
            "status": node.status,
            "stage": node.current_stage,
            "subject": node.location.subject,
            "unit": node.location.unit,
            "chapter": node.location.chapter,
            "subtopic": node.location.subtopic,
            "set": node.location.set_number,
            "batch": node.location.batch_number,
            "question_from": node.question_range.question_from,
            "question_to": node.question_range.question_to,
            "question_count": node.question_range.expected_questions,
            "factory_version": node.metadata.factory_version,
            "blueprint_version": node.metadata.blueprint_version,
        }
