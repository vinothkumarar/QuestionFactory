"""
Question Factory OS v2.0
Runtime Controller

File:
    Engine/director/runtime_controller.py

Description
-----------
Central runtime persistence service for Question Factory OS.

Responsibilities
----------------
* Load runtime from disk
* Save runtime safely
* Create runtime if missing
* Validate runtime schema
* Create recovery checkpoints
* Build next runtime state
* Maintain production statistics
* Recover from interrupted manufacturing

The Runtime Controller is the ONLY component allowed to
read or write the runtime state.
"""

from __future__ import annotations

import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Optional

from Engine.models.runtime_model import RuntimeModel


class RuntimeController:
    """
    Runtime persistence and recovery service.

    The Manufacturing Director interacts with runtime
    exclusively through this controller.
    """

    DEFAULT_RUNTIME_FILE = Path("Engine/runtime/runtime.json")

    def __init__(
        self,
        runtime_file: Optional[Path] = None,
    ) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)

        self.runtime_file = (
            runtime_file or self.DEFAULT_RUNTIME_FILE
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def load(self) -> RuntimeModel:
        """
        Load the runtime from disk.

        If no runtime exists, a new runtime is created,
        persisted and returned.
        """

        if not self.runtime_file.exists():

            self.logger.info(
                "Runtime file not found. Creating new runtime."
            )

            runtime = RuntimeModel()

            self.save(runtime)

            return runtime

        with self.runtime_file.open(
            "r",
            encoding="utf-8",
        ) as fp:

            payload = json.load(fp)

        runtime = RuntimeModel.from_dict(payload)

        self.validate(runtime)

        self.logger.info("Runtime loaded successfully")

        return runtime

    def save(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Persist runtime to disk.
        """

        runtime.touch()

        self.runtime_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.runtime_file.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                runtime.to_dict(),
                fp,
                indent=4,
                ensure_ascii=False,
            )

        self.logger.info(
            "Runtime saved successfully."
        )

    def reset(self) -> RuntimeModel:
        """
        Reset the runtime to a clean factory state.
        """

        runtime = RuntimeModel()

        self.save(runtime)

        self.logger.info(
            "Runtime reset completed."
        )

        return runtime
            # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Validate the runtime model before it is used.

        Raises
        ------
        ValueError
            If the runtime model is invalid.
        """

        if runtime is None:
            raise ValueError("Runtime model cannot be None.")

        if runtime.factory is None:
            raise ValueError("Factory state is missing.")

        if runtime.production is None:
            raise ValueError("Production state is missing.")

        if runtime.statistics is None:
            raise ValueError("Statistics section is missing.")

        if runtime.history is None:
            raise ValueError("History section is missing.")

        if runtime.recovery is None:
            raise ValueError("Recovery section is missing.")

        self.logger.debug("Runtime validation completed successfully.")

    # ---------------------------------------------------------
    # Checkpoint Management
    # ---------------------------------------------------------

    def create_checkpoint(
        self,
        runtime: RuntimeModel,
        stage: str,
    ) -> None:
        """
        Persist a recovery checkpoint.

        Parameters
        ----------
        runtime
            Active runtime model.

        stage
            Manufacturing stage being checkpointed.
        """

        runtime.create_checkpoint(stage)

        self.save(runtime)

        self.logger.info(
            "Checkpoint created for stage '%s'.",
            stage,
        )

    # ---------------------------------------------------------
    # Recovery
    # ---------------------------------------------------------

    def recovery_required(
        self,
        runtime: RuntimeModel,
    ) -> bool:
        """
        Determine whether runtime recovery is required.
        """

        return runtime.is_recovery_required

    def recover(
        self,
        runtime: RuntimeModel,
    ) -> RuntimeModel:
        """
        Recover an interrupted manufacturing cycle.

        Current implementation restores the runtime back to an
        executable state while preserving recovery metadata.

        Future versions may restore pipeline execution from
        intermediate checkpoints.
        """

        if not runtime.is_recovery_required:

            self.logger.info(
                "Runtime recovery not required."
            )

            return runtime

        self.logger.warning(
            "Recovery requested from stage '%s'.",
            runtime.recovery.resume_from_stage,
        )

        runtime.factory.status = "RECOVERING"

        runtime.recovery.retry_count += 1

        runtime.touch()

        self.save(runtime)

        return runtime

    # ---------------------------------------------------------
    # Runtime Backup
    # ---------------------------------------------------------

    def backup(
        self,
        runtime: RuntimeModel,
    ) -> Path:
        """
        Create a timestamped runtime backup.

        Returns
        -------
        Path
            Backup file path.
        """

        backup_directory = (
            self.runtime_file.parent / "backups"
        )

        backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = (
            backup_directory /
            f"runtime_{timestamp}.json"
        )

        with backup_file.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                runtime.to_dict(),
                fp,
                indent=4,
                ensure_ascii=False,
            )

        self.logger.info(
            "Runtime backup created: %s",
            backup_file,
        )

        return backup_file

    # ---------------------------------------------------------
    # Clone Operations
    # ---------------------------------------------------------

    def clone(
        self,
        runtime: RuntimeModel,
    ) -> RuntimeModel:
        """
        Create a deep copy of the runtime model.

        Useful for simulations, dry runs, and planning.
        """

        return deepcopy(runtime)
            # ---------------------------------------------------------
    # Runtime Progression
    # ---------------------------------------------------------

    def build_next_runtime(
        self,
        current_runtime: RuntimeModel,
        production_node,
        package_result,
    ) -> RuntimeModel:
        """
        Build the next runtime state after a successful
        manufacturing cycle.

        The current runtime instance is never modified directly.
        A cloned instance is updated and returned.
        """

        runtime = self.clone(current_runtime)

        self._update_history(
            runtime=runtime,
            production_node=production_node,
        )

        self._update_statistics(
            runtime=runtime,
            package_result=package_result,
        )

        self._advance_production(
            runtime=runtime,
            production_node=production_node,
        )

        runtime.reset_cycle()

        runtime.touch()

        return runtime

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _update_history(
        self,
        runtime: RuntimeModel,
        production_node,
    ) -> None:
        """
        Persist information about the batch that has just
        completed manufacturing.
        """

        history = runtime.history
        production = runtime.production

        history.last_subject = production.subject
        history.last_unit = production.unit
        history.last_chapter = production.chapter
        history.last_subtopic = production.subtopic

        history.last_set_number = production.set_number
        history.last_batch_number = production.batch_number

        history.last_batch_id = production.batch_id
        history.last_production_node = production.production_node

        history.last_completed_at = (
            datetime.utcnow().isoformat()
        )

        history.last_status = "SUCCESS"

    def _update_statistics(
        self,
        runtime: RuntimeModel,
        package_result,
    ) -> None:
        """
        Update cumulative factory statistics.

        Statistics are intentionally cumulative and never reset.
        """

        statistics = runtime.statistics
        production = runtime.production

        statistics.total_batches += 1

        question_count = (
            production.question_to
            - production.question_from
            + 1
        )

        statistics.total_questions += question_count

        if hasattr(package_result, "duration_seconds"):

            duration = package_result.duration_seconds

            statistics.last_batch_duration_seconds = duration

            statistics.total_runtime_seconds += duration

            if statistics.total_batches > 0:

                statistics.average_batch_time_seconds = (
                    statistics.total_runtime_seconds
                    / statistics.total_batches
                )

    def _advance_production(
        self,
        runtime: RuntimeModel,
        production_node,
    ) -> None:
        """
        Advance the runtime to the next production position.

        The scheduler determines *where* to manufacture.

        The Runtime Controller records that decision.
        """

        production = runtime.production

        if hasattr(production_node, "subject"):
            production.subject = production_node.subject

        if hasattr(production_node, "unit"):
            production.unit = production_node.unit

        if hasattr(production_node, "chapter"):
            production.chapter = production_node.chapter

        if hasattr(production_node, "subtopic"):
            production.subtopic = production_node.subtopic

        if hasattr(production_node, "set_number"):
            production.set_number = (
                production_node.set_number
            )

        if hasattr(production_node, "batch_number"):
            production.batch_number = (
                production_node.batch_number
            )

        if hasattr(production_node, "question_from"):
            production.question_from = (
                production_node.question_from
            )

        if hasattr(production_node, "question_to"):
            production.question_to = (
                production_node.question_to
            )

        if hasattr(production_node, "batch_id"):
            production.batch_id = (
                production_node.batch_id
            )

        if hasattr(production_node, "production_node"):
            production.production_node = (
                production_node.production_node
            )

        production.next_question_number = (
            production.question_to + 1
        )

        runtime.touch()
            # ---------------------------------------------------------
    # Runtime Status Management
    # ---------------------------------------------------------

    def begin_cycle(
        self,
        runtime: RuntimeModel,
        cycle_id: str,
    ) -> RuntimeModel:
        """
        Mark the beginning of a manufacturing cycle.
        """

        runtime.start_cycle(cycle_id)

        self.save(runtime)

        self.logger.info(
            "Manufacturing cycle started (%s).",
            cycle_id,
        )

        return runtime

    def complete_cycle(
        self,
        runtime: RuntimeModel,
    ) -> RuntimeModel:
        """
        Mark the current manufacturing cycle as completed.
        """

        runtime.complete_cycle()

        self.save(runtime)

        self.logger.info(
            "Manufacturing cycle completed."
        )

        return runtime

    def fail_cycle(
        self,
        runtime: RuntimeModel,
        reason: str,
    ) -> RuntimeModel:
        """
        Mark the current manufacturing cycle as failed.
        """

        runtime.mark_failed(reason)

        self.save(runtime)

        self.logger.error(
            "Manufacturing cycle failed: %s",
            reason,
        )

        return runtime

    # ---------------------------------------------------------
    # Runtime Information
    # ---------------------------------------------------------

    def exists(self) -> bool:
        """
        Determine whether the runtime file exists.
        """

        return self.runtime_file.exists()

    def runtime_path(self) -> Path:
        """
        Return the runtime file location.
        """

        return self.runtime_file

    def health(self) -> dict:
        """
        Runtime controller health information.
        """

        return {
            "component": self.__class__.__name__,
            "runtime_file": str(self.runtime_file),
            "runtime_exists": self.exists(),
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ---------------------------------------------------------
    # Convenience APIs
    # ---------------------------------------------------------

    def increment_repair_count(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Record one repair cycle.
        """

        runtime.statistics.total_repair_cycles += 1

        runtime.statistics.repaired_batches += 1

        runtime.touch()

    def update_last_stage(
        self,
        runtime: RuntimeModel,
        stage: str,
    ) -> None:
        """
        Record the last successfully completed stage.
        """

        runtime.recovery.last_successful_stage = stage

        runtime.touch()

    def clear_recovery(
        self,
        runtime: RuntimeModel,
    ) -> None:
        """
        Clear recovery information after successful completion.
        """

        runtime.recovery.recovery_required = False
        runtime.recovery.interrupted = False
        runtime.recovery.interruption_reason = ""
        runtime.recovery.resume_from_stage = ""
        runtime.recovery.retry_count = 0

        runtime.touch()

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
        runtime: RuntimeModel,
    ) -> dict:
        """
        Produce a concise runtime summary suitable for logs,
        dashboards, or CLI output.
        """

        return {
            "factory_status": runtime.factory.status,
            "production_node": runtime.production.production_node,
            "batch_id": runtime.production.batch_id,
            "unit": runtime.production.unit,
            "chapter": runtime.production.chapter,
            "subtopic": runtime.production.subtopic,
            "set_number": runtime.production.set_number,
            "batch_number": runtime.production.batch_number,
            "questions": (
                f"{runtime.production.question_from}"
                f"-{runtime.production.question_to}"
            ),
            "total_batches": runtime.statistics.total_batches,
            "total_questions": runtime.statistics.total_questions,
            "recovery_required": (
                runtime.recovery.recovery_required
            ),
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"RuntimeController("
            f"runtime_file='{self.runtime_file}')"
        )

    def __str__(self) -> str:
        return (
            f"RuntimeController[{self.runtime_file}]"
        )
        