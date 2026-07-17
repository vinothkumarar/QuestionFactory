"""
Question Factory OS
Runtime Repository
"""

from Engine.core.runtime_manager import RuntimeManager


class RuntimeRepository:

    def __init__(self):

        self.manager = RuntimeManager()

    def get_runtime(self):

        return self.manager.load()

    def save_runtime(self, runtime: dict):

        self.manager.save(runtime)
