"""
Question Factory OS v3.1

Academic Analyzer

Responsible for performing AI-driven academic analysis
for a single production order.

Responsibilities
----------------
• Build AIJob
• Execute AI analysis
• Return raw academic analysis

Question generation is NOT performed here.
"""

from __future__ import annotations

import logging
from typing import Any


from Engine.factory.ai.ai_engine import (
    AIEngine,
)

from Engine.factory.ai.models.ai_job import (
    AIJob,
)

from Engine.models.production_order_model import (
    ProductionOrderModel,
)

from Engine.factory.planning.models.academic_analysis_model import (
    AcademicAnalysisModel,
)
from Engine.curriculum.runtime.curriculum_context_service import (
    CurriculumContextService,
)

logger = logging.getLogger(__name__)


class AcademicAnalyzer:
    """
    AI driven academic planner.

    This component asks the AI to analyse
    the academic richness of a subtopic.

    It does NOT generate questions.
    """

    def __init__(
        self,
        ai_engine: AIEngine,
    ) -> None:

        self._ai_engine = ai_engine
        self._curriculum = CurriculumContextService()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def analyze(
        self,
        order: ProductionOrderModel,
    ) -> AcademicAnalysisModel:
        """
        Perform academic analysis.
        """

        job = self._build_job(
            order,
        )

        logger.info(
            "Academic analysis started for '%s'.",
            order.subtopic,
        )

        response = self._ai_engine.execute(
            job,
        )

        self.validate_response(
            response,
        )

        parsed_data = (
            self._extract_response_data(
                response,
            )
        )

        print("\nACADEMIC ANALYZER PARSED DATA:\n", parsed_data)
        return AcademicAnalysisModel.from_dict(
            parsed_data,
        )
    # ---------------------------------------------------------
    # AI Job
    # ---------------------------------------------------------

    def _build_job(
        self,
        order: ProductionOrderModel,
    ) -> AIJob:

        return AIJob(
            job_type="ACADEMIC_ANALYSIS",

            project="Question Factory",

            subject=order.subject,

            unit=order.unit,

            chapter=order.chapter,

            subtopic=order.subtopic,

            batch=str(
                order.batch_no,
            ),

            question_count=order.question_count,

            system_prompt=self._system_prompt(),

            user_prompt=self._user_prompt(
                order,
            ),

            response_schema="academic_analysis",

            temperature=0.2,
        )
    # ---------------------------------------------------------
    # Prompt Templates
    # ---------------------------------------------------------

    def _system_prompt(
        self,
    ) -> str:
        """
        System prompt for academic planning.
        """

        return """
You are an IIT JEE Academic Planning Expert.

Your responsibility is NOT to generate questions.

Analyse ONLY the supplied subtopic.

Determine:

1. Academic richness.
2. Estimated total manufacturable questions.
3. Difficulty distribution.
4. Archetype distribution.
5. Important manufacturing recommendations.

Return structured JSON only.

Do not include explanations outside JSON.
""".strip()

    def _user_prompt(
        self,
        order: ProductionOrderModel,
    ) -> str:
        """
        Build the academic analysis prompt.
        """
        context = self._curriculum.enrich(
            order,
        )

        return (
            f"Subject Code : {order.subject}\n"
            f"Subject Name : {context['subject_name']}\n\n"

            f"Unit Code : {order.unit}\n"
            f"Unit Name : {context['unit_name']}\n\n"

            f"Chapter Code : {order.chapter}\n"
            f"Chapter Name : {context['chapter_name']}\n\n"

            f"Subtopic Code : {order.subtopic}\n"
            f"Subtopic Name : {context['subtopic_name']}\n\n"
            f"Set : {order.set_no}\n"
            f"Requested Questions : "
            f"{order.question_count}\n\n"
            "Perform an academic manufacturing analysis.\n\n"
            "Return JSON in the following format:\n\n"
            "{\n"
            '  "estimated_total_questions": integer,\n'
            '  "difficulty_distribution": {\n'
            '      "Easy": integer,\n'
            '      "Medium": integer,\n'
            '      "Hard": integer\n'
            "  },\n"
            '  "archetype_distribution": {\n'
            '      "Conceptual": integer,\n'
            '      "Computational": integer,\n'
            '      "Analytical": integer,\n'
            '      "Application": integer\n'
            "  },\n"
            '  "analysis_summary": "string",\n'
            '  "manufacturing_notes": [\n'
            '      "note1",\n'
            '      "note2"\n'
            "  ]\n"
            "}\n"
        )
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------
    def _extract_response_data(
        self,
        response: Any,
    ) -> dict[str, Any]:
        """
        Convert AI response into a dictionary.
        """

        if isinstance(
            response,
            dict,
        ):
            return response

        raw_json = getattr(
            response,
            "raw_json",
            None,
        )

        if isinstance(
            raw_json,
            dict,
        ):
            return raw_json

        raise TypeError(
            f"Unsupported response type: {type(response).__name__}"
        )

    def validate_response(
        self,
        response: Any,
    ) -> None:
        """
        Validate AI response.
        """

        if response is None:
            raise RuntimeError(
                "Academic analyzer returned no response."
            )

    # ---------------------------------------------------------
    # Convenience API
    # ---------------------------------------------------------

    def analyze_safe(
        self,
        order: ProductionOrderModel,
    ) -> AcademicAnalysisModel:
        """
        Execute academic analysis with validation.
        """

        try:

            response = self.analyze(
                order,
            )

            logger.info(
                "Academic analysis completed."
            )

            return response

        except Exception:

            logger.exception(
                "Academic analysis failed."
            )

            raise

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return AcademicAnalyzer health.
        """

        return {
            "component": "AcademicAnalyzer",
            "status": "READY",
            "ai_engine": (
                self._ai_engine.__class__.__name__
            ),
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return diagnostics.
        """

        return {
            "component": "AcademicAnalyzer",
            "health": self.health(),
            "supported_job": (
                "ACADEMIC_ANALYSIS"
            ),
        }

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        logger.info(
            "AcademicAnalyzer reset."
        )

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    @property
    def component_name(
        self,
    ) -> str:
        return self.__class__.__name__


__all__ = [
    "AcademicAnalyzer",
]
