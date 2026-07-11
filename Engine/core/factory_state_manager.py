"""
Question Factory OS
Factory State Manager

Milestone : M10
Sprint    : S1
Release   : R2
"""


from models.factory_state_model import FactoryStateModel


class FactoryStateManager:

    def get_question_start(
        self,
        state: FactoryStateModel
    ) -> int:

        return (

            (state.current_batch - 1)

            * state.questions_per_batch

            + 1

        )

    def get_question_end(
        self,
        state: FactoryStateModel
    ) -> int:

        return (

            self.get_question_start(state)

            + state.questions_per_batch

            - 1

        )

    def get_next_batch(
        self,
        state: FactoryStateModel
    ) -> int:

        return state.current_batch + 1

    def advance_batch(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:

        state.current_batch += 1

        return state

    def complete_batch(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:
        """
        Called after an entire batch has been
        successfully generated, validated and exported.
        """

        state.current_batch += 1

        state.status = "READY"

        return state

    def set_running(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:

        state.status = "RUNNING"

        return state

    def set_completed(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:

        state.status = "COMPLETED"

        return state

    def set_failed(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:

        state.status = "FAILED"

        return state