"""
Question Factory OS
Production Queue
"""

from collections import deque


class ProductionQueue:

    def __init__(self):

        self.queue = deque()

    def add(self, production_order):

        self.queue.append(production_order)

    def get(self):

        if not self.queue:

            return None

        return self.queue.popleft()

    def size(self):

        return len(self.queue)

    def is_empty(self):

        return len(self.queue) == 0