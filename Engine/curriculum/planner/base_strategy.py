"""
Question Factory OS v2.4
Base Manufacturing Strategy

Milestone : M14
Sprint    : S2
Release   : R1
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from Engine.curriculum.manufacturing_queue import ManufacturingQueue
from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)


class BaseManufacturingStrategy(ABC):
    """
    Base contract for all curriculum
    manufacturing strategies.
    """

    @abstractmethod
    def build(
        self,
        request: ManufacturingRequestModel,
    ) -> ManufacturingQueue:
        """
        Build a manufacturing queue from
        a manufacturing request.
        """
        raise NotImplementedError