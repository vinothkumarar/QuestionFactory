"""
Question Factory OS
Production Queue Model

Milestone : M9
Sprint    : S3
Release   : R1
"""

from dataclasses import dataclass
from dataclasses import field

from models.production_order_model import ProductionOrderModel
from models.production_request_model import ProductionRequestModel


@dataclass
class ProductionQueueModel:

    request: ProductionRequestModel

    orders: list[ProductionOrderModel] = field(default_factory=list)

    total_batches: int = 0

    total_questions: int = 0
