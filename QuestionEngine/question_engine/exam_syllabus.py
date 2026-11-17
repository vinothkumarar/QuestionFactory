"""Auditable, exam-versioned official syllabus source and mapping registry.

This registry never infers approval from a curriculum label. Only explicitly
reviewed mappings backed by a registered official source are eligible.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


class ExamSyllabusRegistryError(ValueError):
    """Raised when syllabus source or mapping data is incomplete or inconsistent."""


@dataclass(frozen=True)
class ExamSyllabusSource:
    source_id: str
    exam: str
    syllabus_version: str
    official_source_title: str
    official_source_url: str
    publication_date: str = ""
    effective_from: str = ""
    effective_to: str = ""
    retrieved_at: str = ""
    document_sha256: str = ""


@dataclass(frozen=True)
class ExamSyllabusMapping:
    mapping_id: str
    source_id: str
    exam: str
    syllabus_version: str
    subject_id: str
    official_wording: str
    curriculum_subtopic_code: str
    review_status: str
    reviewer_id: str = ""
    reviewed_at: str = ""
    review_source: str = ""
    approval_rationale: str = ""


class ExamSyllabusRegistry:
    SOURCE_COLUMNS = {
        "source_id", "exam", "syllabus_version", "official_source_title",
        "official_source_url", "publication_date", "effective_from",
        "effective_to", "retrieved_at", "document_sha256",
    }
    MAPPING_COLUMNS = {
        "mapping_id", "source_id", "exam", "syllabus_version", "subject_id",
        "official_wording", "curriculum_subtopic_code", "review_status",
        "reviewer_id", "reviewed_at", "review_source", "approval_rationale",
    }
    STATUSES = {"PROVISIONAL_REVIEW_REQUIRED", "APPROVED", "REJECTED"}

    def __init__(
        self,
        sources: Iterable[ExamSyllabusSource],
        mappings: Iterable[ExamSyllabusMapping],
    ) -> None:
        self.sources = tuple(sources)
        self.mappings = tuple(mappings)
        source_ids: set[str] = set()
        for source in self.sources:
            if source.source_id in source_ids:
                raise ExamSyllabusRegistryError(f"Duplicate source_id: {source.source_id}")
            source_ids.add(source.source_id)
            required = (
                source.source_id, source.exam, source.syllabus_version,
                source.official_source_title, source.official_source_url,
            )
            if not all(value.strip() for value in required):
                raise ExamSyllabusRegistryError("Syllabus sources require identity, official URL, title and dates")
            if not source.official_source_url.startswith("https://"):
                raise ExamSyllabusRegistryError(f"Official source URL must use HTTPS: {source.source_id}")
            if source.publication_date:
                self._date(source.publication_date, "publication_date", source.source_id)
            start = self._date(source.effective_from, "effective_from", source.source_id) if source.effective_from else None
            end = self._date(source.effective_to, "effective_to", source.source_id) if source.effective_to else None
            if end and start is None:
                raise ExamSyllabusRegistryError(f"effective_to requires effective_from: {source.source_id}")
            if end and start and end < start:
                raise ExamSyllabusRegistryError(f"effective_to precedes effective_from: {source.source_id}")
            if source.retrieved_at:
                self._datetime(source.retrieved_at, "retrieved_at", source.source_id)
            if source.document_sha256 and not re.fullmatch(r"[0-9a-fA-F]{64}", source.document_sha256):
                raise ExamSyllabusRegistryError(f"Invalid document_sha256: {source.source_id}")

        mapping_ids: set[str] = set()
        for mapping in self.mappings:
            if mapping.mapping_id in mapping_ids:
                raise ExamSyllabusRegistryError(f"Duplicate mapping_id: {mapping.mapping_id}")
            mapping_ids.add(mapping.mapping_id)
            if mapping.source_id not in source_ids:
                raise ExamSyllabusRegistryError(
                    f"Mapping {mapping.mapping_id} references unknown source_id {mapping.source_id}"
                )
            source = next(item for item in self.sources if item.source_id == mapping.source_id)
            if (mapping.exam, mapping.syllabus_version) != (source.exam, source.syllabus_version):
                raise ExamSyllabusRegistryError(
                    f"Mapping {mapping.mapping_id} exam/version does not match its source"
                )
            if not all((
                mapping.exam, mapping.syllabus_version, mapping.subject_id,
                mapping.official_wording, mapping.curriculum_subtopic_code,
            )):
                raise ExamSyllabusRegistryError(f"Mapping {mapping.mapping_id} has blank required fields")
            if mapping.review_status not in self.STATUSES:
                raise ExamSyllabusRegistryError(
                    f"Unsupported review_status for {mapping.mapping_id}: {mapping.review_status}"
                )
            if mapping.review_status == "APPROVED":
                if not source.document_sha256 or not source.retrieved_at:
                    raise ExamSyllabusRegistryError(
                        f"APPROVED mapping {mapping.mapping_id} requires a retrieved and "
                        "SHA-256-fingerprinted official source document"
                    )
                if not source.effective_from:
                    raise ExamSyllabusRegistryError(
                        f"APPROVED mapping {mapping.mapping_id} requires an explicit "
                        "effective_from date for the official syllabus source"
                    )
            if mapping.review_status != "PROVISIONAL_REVIEW_REQUIRED":
                audit = (
                    mapping.reviewer_id, mapping.reviewed_at,
                    mapping.review_source, mapping.approval_rationale,
                )
                if not all(value.strip() for value in audit):
                    raise ExamSyllabusRegistryError(
                        f"{mapping.review_status} mapping {mapping.mapping_id} requires reviewer, "
                        "timestamp, review source and rationale"
                    )
                self._datetime(mapping.reviewed_at, "reviewed_at", mapping.mapping_id)

    @staticmethod
    def _date(value: str, field: str, record_id: str) -> date:
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ExamSyllabusRegistryError(
                f"Invalid ISO date {field} for {record_id}: {value}"
            ) from exc

    @staticmethod
    def _datetime(value: str, field: str, record_id: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ExamSyllabusRegistryError(
                f"Invalid ISO-8601 {field} for {record_id}: {value}"
            ) from exc
        if parsed.tzinfo is None:
            raise ExamSyllabusRegistryError(f"{field} must include a timezone for {record_id}")
        return parsed

    @classmethod
    def load_csv(cls, sources_path: Path | str, mappings_path: Path | str) -> "ExamSyllabusRegistry":
        sources = cls._read_csv(Path(sources_path), cls.SOURCE_COLUMNS)
        mappings = cls._read_csv(Path(mappings_path), cls.MAPPING_COLUMNS)
        return cls(
            (ExamSyllabusSource(**row) for row in sources),
            (ExamSyllabusMapping(**row) for row in mappings),
        )

    @staticmethod
    def _read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
        if not path.is_file():
            raise FileNotFoundError(f"Exam syllabus registry file not found: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = required - set(reader.fieldnames or ())
            if missing:
                raise ExamSyllabusRegistryError(
                    f"{path}: missing columns: {', '.join(sorted(missing))}"
                )
            return [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
            ]

    def approved_mapping(
        self, exam: str, syllabus_version: str, subject_id: str,
        curriculum_subtopic_code: str,
    ) -> ExamSyllabusMapping | None:
        """Return one exact approved mapping; ambiguity is an error, not a guess."""
        matches = [
            item for item in self.mappings
            if item.exam == exam
            and item.syllabus_version == syllabus_version
            and item.subject_id == subject_id
            and item.curriculum_subtopic_code == curriculum_subtopic_code
            and item.review_status == "APPROVED"
        ]
        if len(matches) > 1:
            raise ExamSyllabusRegistryError(
                f"Ambiguous approved mappings for {exam}/{syllabus_version}/"
                f"{subject_id}/{curriculum_subtopic_code}"
            )
        return matches[0] if matches else None

    def pending_mappings(self) -> tuple[ExamSyllabusMapping, ...]:
        return tuple(
            item for item in self.mappings
            if item.review_status == "PROVISIONAL_REVIEW_REQUIRED"
        )

    def provisional_baseline_source(
        self, exam: str, target_syllabus_version: str
    ) -> ExamSyllabusSource | None:
        """Return the latest registered prior-year source for comparison only.

        This helper deliberately does not approve a syllabus mapping, verify a
        source document hash, or authorize question generation. The caller must
        preserve the returned source version and label any comparison provisional.
        """
        if not re.fullmatch(r"\d{4}", target_syllabus_version):
            raise ExamSyllabusRegistryError(
                f"Target syllabus version must be a four-digit year: {target_syllabus_version}"
            )
        target_year = int(target_syllabus_version)
        candidates: list[tuple[int, ExamSyllabusSource]] = []
        for source in self.sources:
            if source.exam != exam or not re.fullmatch(r"\d{4}", source.syllabus_version):
                continue
            source_year = int(source.syllabus_version)
            if source_year < target_year:
                candidates.append((source_year, source))
        if not candidates:
            return None
        latest_year = max(year for year, _ in candidates)
        latest = [source for year, source in candidates if year == latest_year]
        if len(latest) != 1:
            raise ExamSyllabusRegistryError(
                f"Ambiguous prior-year baseline sources for {exam}/{target_syllabus_version}: "
                f"{latest_year}"
            )
        return latest[0]


class ExamVersionedQuestionScopeVerifier:
    """Require reviewed official syllabus mappings for every requested exam."""

    METHOD = "exam-versioned-official-syllabus-v1"

    def __init__(self, curriculum, base_verifier, registry, exam_versions):
        self.curriculum = curriculum
        self.base_verifier = base_verifier
        self.registry = registry
        self.exam_versions = dict(exam_versions)

    def verify(self, question):
        from .scope_verification import ScopeVerificationResult

        base = self.base_verifier.verify(question)
        if not base.verified:
            return ScopeVerificationResult(
                question.question_id, False, self.METHOD, "",
                "Internal curriculum/concept check failed: " + base.reason,
            )
        if not question.exam_targets:
            return ScopeVerificationResult(
                question.question_id, False, self.METHOD, "",
                "Question has no exam_targets; exam-specific scope cannot be verified",
            )
        subtopic = next(
            (row for row in self.curriculum.subtopics if row.get("id") == question.subtopic_id),
            None,
        )
        if subtopic is None:
            return ScopeVerificationResult(
                question.question_id, False, self.METHOD, "",
                "Question subtopic_id is not present in the loaded curriculum",
            )
        evidence = [base.evidence]
        for exam in question.exam_targets:
            version = self.exam_versions.get(exam, "")
            if not version:
                return ScopeVerificationResult(
                    question.question_id, False, self.METHOD, "",
                    f"No explicitly configured syllabus version for exam target: {exam}",
                )
            mapping = self.registry.approved_mapping(
                exam, version, question.subject_id, subtopic.get("code", "")
            )
            if mapping is None:
                return ScopeVerificationResult(
                    question.question_id, False, self.METHOD, "",
                    f"No unique APPROVED official syllabus mapping for "
                    f"{exam}/{version}/{question.subject_id}/{subtopic.get('code', '')}",
                )
            evidence.append(
                f"{exam} {version}: {mapping.official_wording} "
                f"(source {mapping.source_id}; review {mapping.review_source})"
            )
        return ScopeVerificationResult(
            question.question_id, True, self.METHOD, "; ".join(evidence)
        )
