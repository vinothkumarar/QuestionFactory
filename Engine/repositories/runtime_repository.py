"""
Question Factory OS v2.2

Runtime Repository
"""

from __future__ import annotations

from Engine.core.runtime_manager import RuntimeManager
from Engine.models.runtime_model import RuntimeModel


class RuntimeRepository:
    """
    Repository responsible for loading and saving
    the strongly typed RuntimeModel.
    """

    def __init__(self) -> None:
        self.manager = RuntimeManager()

    def get_runtime(self) -> RuntimeModel:
        """
        Load runtime.json and convert it into
        a RuntimeModel.
        """

        runtime = self.manager.load()

        return RuntimeModel.from_dict(runtime)

    def save_runtime(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Persist the RuntimeModel back to runtime.json.
        """

        self.manager.save(
            runtime.to_dict()
        )
        