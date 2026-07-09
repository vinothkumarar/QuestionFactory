"""
Question Factory OS
Job Queue
"""

from collections import deque


class JobQueue:

    def __init__(self):

        self.queue = deque()

    def add(self, job):

        self.queue.append(job)

    def get(self):

        if not self.queue:

            return None

        return self.queue.popleft()

    def size(self):

        return len(self.queue)

    def is_empty(self):

        return len(self.queue) == 0
        