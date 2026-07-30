"""
Question Factory OS v3.0

Production Manufacturing Entry Point

Responsibilities
----------------
1. Load environment.
2. Parse CLI arguments.
3. Build ManufacturingRequestModel.
4. Build ManufacturingQueue.
5. Execute ProductionOrchestrator.
6. Print manufacturing summary.

The entry point contains NO business logic.
"""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Sequence

from dotenv import load_dotenv

from Engine.curriculum.planner.curriculum_manufacturing_planner import (
    CurriculumManufacturingPlanner,
)

from Engine.curriculum.manufacturing_request_model import (
    ManufacturingRequestModel,
)

from Engine.curriculum.manufacturing_scope import (
    ManufacturingScope,
)

from Engine.curriculum.runtime.factory_runtime_service import (
    FactoryRuntimeService,
)

from Engine.curriculum.integration.curriculum_production_planner import (
    CurriculumProductionPlanner,
)

from Engine.factory.factory_runner import (
    FactoryRunner,
)

from Engine.curriculum.orchestrator.production_orchestrator import (
    ProductionOrchestrator,
)

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------


def build_argument_parser() -> argparse.ArgumentParser:
    """
    Build the Question Factory CLI.
    """

    parser = argparse.ArgumentParser(
        prog="Question Factory",
        description=(
            "Question Factory OS v3.0 "
            "Autonomous Manufacturing"
        ),
    )

    parser.add_argument(
        "--scope",
        required=True,
        choices=[
            scope.value
            for scope in ManufacturingScope
        ],
        help="Manufacturing scope.",
    )

    parser.add_argument(
        "--subject",
        required=True,
        help="Subject name.",
    )

    parser.add_argument(
        "--unit",
        default="",
        help="Unit code.",
    )

    parser.add_argument(
        "--chapter",
        default="",
        help="Chapter code.",
    )

    parser.add_argument(
        "--subtopic",
        default="",
        help="Subtopic code.",
    )

    parser.add_argument(
        "--start-set",
        default="S1",
    )

    parser.add_argument(
        "--end-set",
        default="S5",
    )

    parser.add_argument(
        "--start-batch",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--end-batch",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--questions-per-batch",
        type=int,
        default=20,
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help=(
            "Continue manufacturing even if a "
            "work item fails."
        ),
    )

    return parser


# ---------------------------------------------------------
# Request Builder
# ---------------------------------------------------------


def build_request(
    args: argparse.Namespace,
) -> ManufacturingRequestModel:
    """
    Convert CLI arguments into a
    ManufacturingRequestModel.
    """

    return ManufacturingRequestModel(
        scope=ManufacturingScope(args.scope),
        subject=args.subject,
        unit=args.unit,
        chapter=args.chapter,
        subtopic=args.subtopic,
        start_set=args.start_set,
        end_set=args.end_set,
        start_batch=args.start_batch,
        end_batch=args.end_batch,
        questions_per_batch=args.questions_per_batch,
        stop_on_failure=(
            not args.continue_on_error
        ),
    )
# ---------------------------------------------------------
# Manufacturing Execution
# ---------------------------------------------------------


def execute_request(
    request: ManufacturingRequestModel,
) -> int:
    """
    Execute one manufacturing request.

    Returns
    -------
    int
        Total questions generated.
    """

    LOGGER.info(
        "Building manufacturing queue."
    )

    planner = CurriculumManufacturingPlanner()

    queue = planner.build(
        request,
    )

    LOGGER.info(
        "Manufacturing queue created (%d work items).",
        len(queue),
    )

    runtime_service = (
        FactoryRuntimeService()
    )

    factory_runner = (
        FactoryRunner()
    )

    production_planner = (
        CurriculumProductionPlanner()
    )

    orchestrator = (
        ProductionOrchestrator(
            runtime_service=runtime_service,
            factory_runner=factory_runner,
            planner=production_planner,
        )
    )

    total_questions = 0
    completed = 0
    failed = 0

    print()
    print("=" * 80)
    print("QUESTION FACTORY OS v3.0")
    print("AUTONOMOUS MANUFACTURING")
    print("=" * 80)
    print()

    while queue.has_next:

        work_item = queue.dequeue()

        try:

            LOGGER.info(
                "Executing %s",
                work_item,
            )

            question_count = (
                orchestrator.execute(
                    work_item,
                )
            )

            total_questions += (
                question_count
            )

            completed += 1

        except Exception:

            failed += 1

            LOGGER.exception(
                "Manufacturing failed."
            )

            if request.stop_on_failure:

                raise

    print()
    print("=" * 80)
    print("MANUFACTURING SUMMARY")
    print("=" * 80)
    print()

    print(
        f"Work Items        : {completed + failed}"
    )

    print(
        f"Completed         : {completed}"
    )

    print(
        f"Failed            : {failed}"
    )

    print(
        f"Questions Created : {total_questions}"
    )

    print()

    return total_questions
# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """
    Question Factory application entry point.
    """

    load_dotenv()

    parser = build_argument_parser()

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(message)s"
        ),
    )

    try:

        request = build_request(
            args,
        )

        total_questions = execute_request(
            request,
        )

        LOGGER.info(
            "Manufacturing completed successfully."
        )

        print(
            "=" * 80
        )
        print(
            "PRODUCTION COMPLETED SUCCESSFULLY"
        )
        print(
            "=" * 80
        )
        print()

        print(
            "Questions Generated :",
            total_questions,
        )

        print()

        return 0

    except KeyboardInterrupt:

        LOGGER.warning(
            "Manufacturing cancelled by user."
        )

        return 130

    except Exception as ex:

        LOGGER.exception(
            "Manufacturing failed."
        )

        print()

        print(
            "=" * 80
        )

        print(
            "PRODUCTION FAILED"
        )

        print(
            "=" * 80
        )

        print()

        print(str(ex))

        print()

        return 1


# ---------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------

if __name__ == "__main__":

    sys.exit(
        main()
    )
    
