"""
Question Factory OS
Production Planner
"""

from models.production_order_model import ProductionOrderModel
from planning.production_order_id_generator import ProductionOrderIdGenerator


class ProductionPlanner:

    def __init__(self):

        self.id_generator = ProductionOrderIdGenerator()

    def create(
        self,
        runtime: dict,
        question_count: int = 100
    ) -> ProductionOrderModel:

        order_id = self.id_generator.generate(
            runtime,
            question_count
        )

        return ProductionOrderModel(

            order_id=order_id,

            subject="Physics",

            unit=runtime["current_project"],

            chapter=runtime["current_chapter"],

            subtopic=runtime["current_subtopic"],

            set_no=runtime["current_set"],

            batch_no=runtime["current_batch"],

            question_start=runtime["next_question"],

            question_count=question_count

        )
                