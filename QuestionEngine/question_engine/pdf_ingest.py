"""Local PDF intake with page-level provenance and explicit OCR gaps.

This module extracts page text only. It does not infer question boundaries,
answer keys, diagrams, or missing content from incomplete PDFs.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class PDFPageText:
    page_number: int
    text: str
    needs_ocr: bool
    extraction_error: str = ""


@dataclass(frozen=True)
class PDFExtractionResult:
    source_path: str
    sha256: str
    page_count: int
    pages: tuple[PDFPageText, ...]
    title: str = ""

    @property
    def pages_needing_ocr(self) -> tuple[int, ...]:
        return tuple(page.page_number for page in self.pages if page.needs_ocr)

    @property
    def extracted_text_page_count(self) -> int:
        return sum(bool(page.text.strip()) for page in self.pages)


class PDFTextExtractor:
    """Extract selectable PDF text while preserving original page numbering."""

    def __init__(self, max_file_size_bytes: int = 200 * 1024 * 1024):
        if max_file_size_bytes < 1:
            raise ValueError("max_file_size_bytes must be positive")
        self.max_file_size_bytes = max_file_size_bytes

    def extract(self, source_path: Path | str) -> PDFExtractionResult:
        path = Path(source_path)
        if not path.is_file():
            raise FileNotFoundError(path)
        size = path.stat().st_size
        if size > self.max_file_size_bytes:
            raise ValueError(
                f"PDF exceeds configured size limit ({size} > {self.max_file_size_bytes})"
            )
        if size < 5 or path.read_bytes()[:5] != b"%PDF-":
            raise ValueError(f"File is not a valid PDF header: {path}")

        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)

        reader = PdfReader(str(path), strict=False)
        if reader.is_encrypted:
            raise ValueError(f"Encrypted PDF requires a separately authorized password: {path}")

        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
                pages.append(
                    PDFPageText(
                        page_number=page_number,
                        text=text,
                        needs_ocr=not bool(text.strip()),
                    )
                )
            except Exception as exc:  # Preserve page and error instead of losing the paper.
                pages.append(
                    PDFPageText(
                        page_number=page_number,
                        text="",
                        needs_ocr=True,
                        extraction_error=f"{type(exc).__name__}: {exc}",
                    )
                )

        metadata = reader.metadata
        title = str(metadata.title) if metadata and metadata.title else ""
        return PDFExtractionResult(
            source_path=str(path),
            sha256=digest.hexdigest(),
            page_count=len(pages),
            pages=tuple(pages),
            title=title,
        )
