"""OpenAI Chat Completions adapter for original-question generation.

The API key and model are supplied through deployment environment variables.
Generated answers are always marked unverified; the independent verifier remains
a mandatory downstream stage.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .generation import GenerationRequest
from .models import QuestionCandidate, QuestionOrigin, QuestionQualityScores


class OpenAIProviderError(RuntimeError):
    """Raised when the model response cannot safely become candidate records."""


Transport = Callable[[str, Mapping[str, str], bytes, float], bytes]


def _http_transport(
    url: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout: float,
) -> bytes:
    request = Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        # Do not include request headers or secrets in the surfaced error.
        detail = exc.read(2048).decode("utf-8", errors="replace")
        raise OpenAIProviderError(
            f"OpenAI API returned HTTP {exc.code}: {detail}"
        ) from exc
    except URLError as exc:
        raise OpenAIProviderError(f"OpenAI API connection failed: {exc.reason}") from exc


class OpenAIQuestionGenerationProvider:
    """Generate draft original-question candidates through OpenAI's API.

    Required environment:
      OPENAI_API_KEY  secret API key
      OPENAI_MODEL    model ID enabled for the user's API project

    Optional environment:
      OPENAI_BASE_URL API base URL (defaults to https://api.openai.com/v1)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float = 90.0,
        transport: Transport = _http_transport,
    ) -> None:
        self.api_key = (api_key or os.getenv("OPENAI_API_KEY", "")).strip()
        self.model = (model or os.getenv("OPENAI_MODEL", "")).strip()
        self.base_url = (
            base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        ).rstrip("/")
        self.timeout = timeout
        self.transport = transport
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        if not self.model:
            raise ValueError("OPENAI_MODEL is not configured")
        if timeout <= 0:
            raise ValueError("timeout must be positive")

    @staticmethod
    def _messages(request: GenerationRequest) -> list[dict[str, str]]:
        system = (
            "You are an expert entrance-exam question author. Return only a JSON "
            "object with a 'questions' array. Create original questions, not copied "
            "or reconstructed historical questions. Never claim an answer has been "
            "independently verified. Do not invent missing diagrams or source facts. "
            "Each question must be self-contained, unambiguous, syllabus-aligned, "
            "and include a correct worked explanation and four distinct options "
            "for SINGLE_CORRECT MCQs. Use only the supplied curriculum scope."
        )
        payload = {
            "task": "Create a small set of genuinely distinct original question candidates.",
            "curriculum": {
                "subject_id": request.subject_id,
                "unit_id": request.unit_id,
                "chapter_id": request.chapter_id,
                "subtopic_id": request.subtopic_id,
            },
            "exam_targets": list(request.exam_targets),
            "concept_ids": list(request.concept_ids),
            "learning_outcomes": list(request.learning_outcomes),
            "avoid_reasoning_signatures": list(request.excluded_reasoning_signatures),
            "candidate_limit": request.candidate_limit,
            "question_fields": {
                "question_text": "complete student-facing question",
                "answer_type": "SINGLE_CORRECT",
                "options": ["option A", "option B", "option C", "option D"],
                "correct_answer": "exact option text or stable option label",
                "explanation": "complete step-by-step derivation",
                "difficulty": "Foundation|Easy|Medium|Hard|Advanced",
                "concept_ids": ["concept identifiers"],
                "reasoning_signature": "short description of reasoning approach",
                "uniqueness_key": "short concept/archetype uniqueness key",
                "quality_scores": {
                    "academic_accuracy": 0,
                    "reasoning_depth": 0,
                    "clarity": 0,
                    "distractor_quality": 0,
                    "exam_relevance": 0,
                },
                "tags": ["tags"],
            },
            "constraints": [
                "Do not include question_id; the application assigns a draft ID.",
                "Do not include answer_verified or syllabus_scope_verified.",
                "Do not include PYQ provenance or claim the question is a PYQ.",
                "Do not use a fixed template with only changed numbers.",
                "Return fewer questions rather than weak, repetitive, or uncertain ones.",
            ],
        }
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ]

    @staticmethod
    def _candidate(
        item: object,
        request: GenerationRequest,
        index: int,
    ) -> QuestionCandidate:
        if not isinstance(item, dict):
            raise OpenAIProviderError(f"Question candidate {index} is not an object")

        def required_text(name: str) -> str:
            value = item.get(name)
            if not isinstance(value, str) or not value.strip():
                raise OpenAIProviderError(
                    f"Question candidate {index} has missing/invalid {name}"
                )
            return value.strip()

        question_text = required_text("question_text")
        answer_type = required_text("answer_type").upper()
        correct_answer = required_text("correct_answer")
        explanation = required_text("explanation")
        options_value = item.get("options", [])
        if not isinstance(options_value, list) or not all(
            isinstance(option, str) for option in options_value
        ):
            raise OpenAIProviderError(
                f"Question candidate {index} has invalid options"
            )
        options = tuple(option.strip() for option in options_value)
        if answer_type == "SINGLE_CORRECT" and len(options) != 4:
            raise OpenAIProviderError(
                f"Question candidate {index} must contain exactly four options"
            )

        scores_value = item.get("quality_scores")
        scores = None
        if isinstance(scores_value, dict):
            score_names = (
                "academic_accuracy",
                "reasoning_depth",
                "clarity",
                "distractor_quality",
                "exam_relevance",
            )
            if all(isinstance(scores_value.get(name), int) for name in score_names):
                scores = QuestionQualityScores(
                    **{name: scores_value[name] for name in score_names}
                )

        concepts = item.get("concept_ids", [])
        tags = item.get("tags", [])
        if not isinstance(concepts, list) or not all(
            isinstance(value, str) for value in concepts
        ):
            raise OpenAIProviderError(
                f"Question candidate {index} has invalid concept_ids"
            )
        if not isinstance(tags, list) or not all(
            isinstance(value, str) for value in tags
        ):
            raise OpenAIProviderError(f"Question candidate {index} has invalid tags")

        reasoning_signature = required_text("reasoning_signature")
        uniqueness_key = required_text("uniqueness_key")
        draft_id = "DRAFT-" + hashlib.sha256(
            question_text.encode("utf-8")
        ).hexdigest()[:16].upper()

        return QuestionCandidate(
            question_id=draft_id,
            origin=QuestionOrigin.ORIGINAL,
            subject_id=request.subject_id,
            unit_id=request.unit_id,
            chapter_id=request.chapter_id,
            subtopic_id=request.subtopic_id,
            question_text=question_text,
            answer_type=answer_type,
            correct_answer=correct_answer,
            explanation=explanation,
            options=options,
            difficulty=str(item.get("difficulty", "Medium")),
            exam_targets=request.exam_targets,
            concept_ids=tuple(concepts),
            reasoning_signature=reasoning_signature,
            uniqueness_key=uniqueness_key,
            answer_verified=False,
            syllabus_scope_verified=False,
            quality_scores=scores,
            tags=tuple(tags),
        )

    def generate(self, request: GenerationRequest):
        body = json.dumps(
            {
                "model": self.model,
                "messages": self._messages(request),
                "response_format": {"type": "json_object"},
            },
            ensure_ascii=False,
        ).encode("utf-8")
        response_bytes = self.transport(
            f"{self.base_url}/chat/completions",
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            body,
            self.timeout,
        )
        try:
            response = json.loads(response_bytes.decode("utf-8"))
            content = response["choices"][0]["message"]["content"]
            payload = json.loads(content)
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise OpenAIProviderError(
                "OpenAI response did not contain a valid JSON questions payload"
            ) from exc

        if not isinstance(payload, dict) or not isinstance(payload.get("questions"), list):
            raise OpenAIProviderError("OpenAI response is missing the questions array")
        if len(payload["questions"]) > request.candidate_limit:
            raise OpenAIProviderError(
                "OpenAI response exceeded the requested candidate limit"
            )

        for index, item in enumerate(payload["questions"], start=1):
            yield self._candidate(item, request, index)
