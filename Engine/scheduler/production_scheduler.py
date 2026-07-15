"""
Question Factory OS
Production Scheduler

Milestone : M13
Sprint    : S2
Release   : R2

Builds Production Requests from a Production Plan.
"""

from typing import List

from models.production_plan_model import ProductionPlanModel

from models.production_request_model import ProductionRequestModel


class ProductionScheduler:
    """
    Converts a ProductionPlanModel into
    a list of ProductionRequestModel objects.

    One ProductionRequest = One Batch
    """

    def build_schedule(self, plan: ProductionPlanModel) -> List[ProductionRequestModel]:

        requests = []

        question_start = (plan.start_batch - 1) * plan.questions_per_batch + 1

        for batch_no in range(plan.start_batch, plan.end_batch + 1):

            request = ProductionRequestModel(
                request_id=(
                    f"{plan.project}_"
                    f"{plan.chapter}_"
                    f"{plan.subtopic}_"
                    f"{plan.set_no}_"
                    f"B{batch_no}"
                ),
                subject="Physics",
                unit=plan.project,
                chapter=plan.chapter,
                subtopic=plan.subtopic,
                set_no=plan.set_no,
                total_questions=plan.questions_per_batch,
            )

            #
            # Runtime Information
            #

            request.batch_no = batch_no

            request.question_start = question_start

            requests.append(request)

            question_start += plan.questions_per_batch

        return requests
