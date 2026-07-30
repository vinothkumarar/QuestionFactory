"""
Question Factory OS v2.4
Manufacturing Queue

Milestone : M14
Sprint    : S2
Release   : R1

Stores and manages executable manufacturing work items.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Iterator

from Engine.curriculum.manufacturing_work_item_model import (
    ManufacturingWorkItemModel,
)


class ManufacturingQueue:
    """
    FIFO queue of manufacturing work items.

    This class contains no manufacturing logic.
    It simply stores and serves work items.
    """

    def __init__(self) -> None:

        self._queue: Deque[
            ManufacturingWorkItemModel
        ] = deque()

    # ---------------------------------------------------------
    # Queue Operations
    # ---------------------------------------------------------

    def enqueue(
        self,
        item: ManufacturingWorkItemModel,
    ) -> None:

        self._queue.append(item)

    def dequeue(
        self,
    ) -> ManufacturingWorkItemModel:

        if not self._queue:

            raise IndexError(
                "Manufacturing queue is empty."
            )

        return self._queue.popleft()

    def peek(
        self,
    ) -> ManufacturingWorkItemModel:

        if not self._queue:

            raise IndexError(
                "Manufacturing queue is empty."
            )

        return self._queue[0]

    def clear(
        self,
    ) -> None:

        self._queue.clear()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def size(
        self,
    ) -> int:

        return len(self._queue)

    @property
    def is_empty(
        self,
    ) -> bool:

        return len(self._queue) == 0

    @property
    def has_next(
        self,
    ) -> bool:

        return len(self._queue) > 0

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[ManufacturingWorkItemModel]:

        return iter(self._queue)

    def __len__(
        self,
    ) -> int:

        return len(self._queue)

    def __repr__(
        self,
    ) -> str:

        return (
            f"ManufacturingQueue("
            f"size={len(self._queue)})"
        )
        