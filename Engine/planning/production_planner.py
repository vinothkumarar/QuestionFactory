"""
Question Factory OS
Production Planner
"""

from models.factory_state_model import FactoryStateModel
from models.production_order_model import ProductionOrderModel

from planning.production_order_id_generator import ProductionOrderIdGenerator

from core.factory_state_manager import FactoryStateManager


class ProductionPlanner:

    def __init__(self):

        self.id_generator = ProductionOrderIdGenerator()

        self.state_manager = FactoryStateManager()

    def plan(self, state: FactoryStateModel) -> ProductionOrderModel:

        question_start = self.state_manager.get_question_start(state)

        order_id = self.id_generator.generate(state)

        return ProductionOrderModel(
            order_id=order_id,
            subject="Physics",
            unit=state.project,
            chapter=state.chapter,
            subtopic=state.subtopic,
            set_no=state.set_no,
            batch_no=state.current_batch,
            question_start=question_start,
            question_count=state.questions_per_batch,
            status="PLANNED",
        )
