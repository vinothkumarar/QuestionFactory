"""
Question Factory OS
Queue Builder

Milestone : M10
Sprint    : S1
Rollback  : Restore Original Design
"""

from Engine.models.production_order_model import ProductionOrderModel
from Engine.models.production_queue_model import ProductionQueueModel
from Engine.models.production_request_model import ProductionRequestModel

from Engine.repositories.factory_state_repository import (
    FactoryStateRepository,
)

from Engine.runtime.factory_state_manager import (
    FactoryStateManager,
)


class QueueBuilder:

    def __init__(self):

        self.repository = FactoryStateRepository()

        self.manager = FactoryStateManager()

    def build(self, request: ProductionRequestModel) -> ProductionQueueModel:

        state = self.repository.load()

        queue = ProductionQueueModel(request=request)

        remaining = request.total_questions

        batch = state.current_batch

        while remaining > 0:

            state.current_batch = batch

            question_start = self.manager.get_question_start(state)

            question_count = min(remaining, state.questions_per_batch)

            order = ProductionOrderModel(
                order_id=f"{request.request_id}_B{batch}",
                subject=request.subject,
                unit=request.unit,
                chapter=request.chapter,
                subtopic=request.subtopic,
                set_no=request.set_no,
                batch_no=batch,
                question_start=question_start,
                question_count=question_count,
            )

            queue.orders.append(order)

            remaining -= question_count

            batch += 1

        queue.total_batches = len(queue.orders)

        queue.total_questions = request.total_questions

        return queue
