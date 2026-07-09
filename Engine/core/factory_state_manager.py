"""
Question Factory OS
Factory State Manager
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
        