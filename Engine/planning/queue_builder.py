"""
Question Factory OS
Queue Builder

Milestone : M10
Sprint    : S1
Release   : R1
"""

from models.production_order_model import ProductionOrderModel
from models.production_queue_model import ProductionQueueModel
from models.production_request_model import ProductionRequestModel

from repositories.factory_state_repository import (
    FactoryStateRepository
)

from core.factory_state_manager import (
    FactoryStateManager
)


class QueueBuilder:

    def __init__(self):

        self.repository = FactoryStateRepository()

        self.manager = FactoryStateManager()

    def build(
        self,
        request: ProductionRequestModel
    ) -> ProductionQueueModel:

        state = self.repository.load()

        queue = ProductionQueueModel(
            request=request
        )

        current_batch = state.current_batch

        question_number = self.manager.get_question_start(
            state
        )

        batch_question_count = 0

        for index in range(request.total_questions):

            order = ProductionOrderModel(

                order_id=(
                    f"{request.request_id}"
                    f"_Q{question_number}"
                ),

                subject=request.subject,

                unit=request.unit,

                chapter=request.chapter,

                subtopic=request.subtopic,

                set_no=request.set_no,

                batch_no=current_batch,

                question_start=question_number,

                question_count=1

            )

            queue.orders.append(order)

            queue.total_questions += 1

            batch_question_count += 1

            question_number += 1

            if batch_question_count == state.questions_per_batch:

                queue.total_batches += 1

                current_batch += 1

                batch_question_count = 0

        if batch_question_count > 0:

            queue.total_batches += 1

        return queue
        