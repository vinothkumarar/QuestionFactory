"""
Question Factory OS
Production Order ID Generator
"""

from models.factory_state_model import FactoryStateModel


class ProductionOrderIdGenerator:

    def generate(self, state: FactoryStateModel) -> str:

        question_start = (state.current_batch - 1) * state.questions_per_batch + 1

        question_end = question_start + state.questions_per_batch - 1

        return (
            f"ORDER_"
            f"{state.project}_"
            f"{state.chapter}_"
            f"{state.subtopic}_"
            f"{state.set_no}_"
            f"B{state.current_batch}_"
            f"Q{question_start}_{question_end}"
        )
