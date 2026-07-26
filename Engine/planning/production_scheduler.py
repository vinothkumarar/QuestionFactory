"""
Question Factory OS v2.3

Production Scheduler

Determines the next manufacturing state based on the
current factory state and the production blueprint.

The scheduler never generates questions.
It only decides what should be manufactured next.
"""

from __future__ import annotations

from Engine.models.factory_state_model import FactoryStateModel


class ProductionScheduler:
    """
    Responsible for production progression.

    Future responsibilities
    -----------------------
    - Batch progression
    - Set progression
    - Subtopic progression
    - Chapter progression
    - Unit progression
    - Blueprint completion detection
    """

    def has_work(
        self,
        state: FactoryStateModel,
    ) -> bool:
        """
        Returns True while manufacturing remains.
        """

        return state.status != "COMPLETED"

    def advance(
        self,
        state: FactoryStateModel,
    ) -> FactoryStateModel:
        """
        Advance the factory to the next production state.

        Version 1 simply advances the batch.
        Future versions will use the blueprint
        to determine progression.
        """

        state.current_batch += 1

        return state