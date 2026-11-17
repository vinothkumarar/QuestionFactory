"""Conservative question-boundary detection for extracted PYQ page text.

Fragments retain exact source text and page numbers. They are not promoted to
verified QuestionCandidate records; uncertain boundaries stay pending review.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .pdf_ingest import PDFExtractionResult, PDFPageText


_QUESTION_START = re.compile(
    r"^\s*(?:(?:Q(?:uestion)?\s*)?(\d{1,3})[.)]|Q(?:uestion)?\s*(\d{1,3})\s*[:.)])\s+",
    re.IGNORECASE,
)
_OPTION_START = re.compile(r"^\s*[\[(]?([A-D])[\]).:]\s*", re.IGNORECASE)


@dataclass(frozen=True)
class PYQTextFragment:
    source_path: str
    source_sha256: str
    page_number: int
    question_number: str
    raw_text: str
    detected_option_labels: tuple[str, ...]
    pending_reasons: tuple[str, ...]

    @property
    def needs_manual_review(self) -> bool:
        return bool(self.pending_reasons)


@dataclass(frozen=True)
class PYQSegmentationResult:
    source_path: str
    source_sha256: str
    fragments: tuple[PYQTextFragment, ...]
    pages_without_question_boundaries: tuple[int, ...]


class PYQTextSegmenter:
    """Split only confidently numbered question starts; preserve all raw text."""

    def segment_page(
        self,
        page: PDFPageText,
        source_path: str = "",
        source_sha256: str = "",
    ) -> tuple[PYQTextFragment, ...]:
        lines = page.text.splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = _QUESTION_START.match(line)
            if match:
                number = match.group(1) or match.group(2) or ""
                starts.append((index, number))

        if not starts:
            if not page.text.strip():
                return ()
            return (
                PYQTextFragment(
                    source_path=source_path,
                    source_sha256=source_sha256,
                    page_number=page.page_number,
                    question_number="",
                    raw_text=page.text,
                    detected_option_labels=(),
                    pending_reasons=(
                        "No recognizable numbered question boundary on this page",
                    ),
                ),
            )

        fragments: list[PYQTextFragment] = []
        if lines[: starts[0][0]]:
            preamble = "\n".join(lines[: starts[0][0]]).strip()
            if preamble:
                fragments.append(
                    PYQTextFragment(
                        source_path=source_path,
                        source_sha256=source_sha256,
                        page_number=page.page_number,
                        question_number="",
                        raw_text=preamble,
                        detected_option_labels=(),
                        pending_reasons=("Page preamble requires manual classification",),
                    )
                )

        for position, (start_line, question_number) in enumerate(starts):
            end_line = (
                starts[position + 1][0]
                if position + 1 < len(starts)
                else len(lines)
            )
            raw_text = "\n".join(lines[start_line:end_line]).strip()
            labels: list[str] = []
            for line in lines[start_line + 1 : end_line]:
                option = _OPTION_START.match(line)
                if option:
                    label = option.group(1).upper()
                    if label not in labels:
                        labels.append(label)

            reasons = []
            if len(labels) != 4:
                reasons.append(
                    f"Detected {len(labels)} distinct option labels; expected four for an MCQ"
                )
            if len(raw_text) < 25:
                reasons.append("Extracted fragment is unusually short")
            if position == len(starts) - 1:
                reasons.append(
                    "Last question on page may continue onto the next page; check source"
                )

            fragments.append(
                PYQTextFragment(
                    source_path=source_path,
                    source_sha256=source_sha256,
                    page_number=page.page_number,
                    question_number=question_number,
                    raw_text=raw_text,
                    detected_option_labels=tuple(labels),
                    pending_reasons=tuple(reasons),
                )
            )
        return tuple(fragments)

    def segment_pdf(self, extraction: PDFExtractionResult) -> PYQSegmentationResult:
        fragments: list[PYQTextFragment] = []
        no_boundaries: list[int] = []
        for page in extraction.pages:
            page_fragments = self.segment_page(
                page,
                source_path=extraction.source_path,
                source_sha256=extraction.sha256,
            )
            fragments.extend(page_fragments)
            if page.text.strip() and not any(
                fragment.question_number for fragment in page_fragments
            ):
                no_boundaries.append(page.page_number)
        return PYQSegmentationResult(
            source_path=extraction.source_path,
            source_sha256=extraction.sha256,
            fragments=tuple(fragments),
            pages_without_question_boundaries=tuple(no_boundaries),
        )
