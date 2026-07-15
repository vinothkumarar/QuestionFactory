"""
Question Factory OS v2.0

Blueprint Parser

File
----
Engine/blueprint/blueprint_parser.py

Description
-----------
Converts blueprint markdown documents into a structured,
intermediate representation.

The parser performs syntax extraction only.

It intentionally contains no business logic.

The parsed output is consumed by the BlueprintCompiler.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List

# ---------------------------------------------------------
# Parsed Section
# ---------------------------------------------------------


@dataclass(slots=True)
class ParsedSection:
    """
    Represents a single markdown heading and its content.
    """

    level: int

    title: str

    content: List[str] = field(default_factory=list)


# ---------------------------------------------------------
# Parsed Document
# ---------------------------------------------------------


@dataclass(slots=True)
class ParsedDocument:
    """
    Represents one parsed blueprint markdown document.
    """

    filename: str

    sections: List[ParsedSection] = field(default_factory=list)

    metadata: Dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------
# Blueprint Parser
# ---------------------------------------------------------


class BlueprintParser:
    """
    Parses blueprint markdown into structured documents.
    """

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")

    def __init__(self) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def parse(
        self,
        documents: Dict[str, str],
    ) -> Dict[str, ParsedDocument]:
        """
        Parse all blueprint markdown documents.

        Parameters
        ----------
        documents
            Dictionary of filename -> markdown content.

        Returns
        -------
        Dict[str, ParsedDocument]
        """

        parsed_documents: Dict[
            str,
            ParsedDocument,
        ] = {}

        for filename, markdown in documents.items():

            self.logger.info(
                "Parsing blueprint document: %s",
                filename,
            )

            parsed_documents[filename] = self._parse_document(
                filename,
                markdown,
            )

        self.logger.info(
            "Parsed %d blueprint document(s).",
            len(parsed_documents),
        )

        return parsed_documents
        # -----------------------------------------------------

    # Document Parsing
    # -----------------------------------------------------

    def _parse_document(
        self,
        filename: str,
        markdown: str,
    ) -> ParsedDocument:
        """
        Parse a single markdown document.

        A document is decomposed into a sequence of sections,
        each beginning with a markdown heading.
        """

        document = ParsedDocument(
            filename=filename,
        )

        current_section: ParsedSection | None = None

        for line in markdown.splitlines():

            heading = self.HEADING_PATTERN.match(line)

            if heading:

                # Persist previous section before starting a new one.
                if current_section is not None:
                    document.sections.append(current_section)

                current_section = ParsedSection(
                    level=len(heading.group(1)),
                    title=heading.group(2).strip(),
                )

                continue

            # Ignore leading content before the first heading.
            if current_section is None:
                continue

            current_section.content.append(line)

        # Persist final section.
        if current_section is not None:
            document.sections.append(current_section)

        document.metadata = self._build_metadata(document)

        self.logger.info(
            "Parsed %d section(s) from %s",
            len(document.sections),
            filename,
        )

        return document

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    def _build_metadata(
        self,
        document: ParsedDocument,
    ) -> Dict[str, str]:
        """
        Build lightweight metadata for a parsed document.

        The parser intentionally records only structural
        information. Semantic interpretation belongs to the
        BlueprintCompiler.
        """

        return {
            "filename": document.filename,
            "section_count": str(len(document.sections)),
            "parser": self.__class__.__name__,
        }

    # -----------------------------------------------------
    # Section Helpers
    # -----------------------------------------------------

    def section_titles(
        self,
        document: ParsedDocument,
    ) -> List[str]:
        """
        Return the section titles in document order.
        """

        return [section.title for section in document.sections]

    def find_section(
        self,
        document: ParsedDocument,
        title: str,
    ) -> ParsedSection | None:
        """
        Locate a section by title.

        Matching is case-insensitive.
        """

        lookup = title.casefold()

        for section in document.sections:

            if section.title.casefold() == lookup:
                return section

        return None
        # -----------------------------------------------------

    # Markdown Element Extraction
    # -----------------------------------------------------

    def extract_bullet_lists(
        self,
        section: ParsedSection,
    ) -> List[str]:
        """
        Extract markdown bullet items from a section.

        Supports:
            - item
            * item
            + item
        """

        items: List[str] = []

        for line in section.content:

            stripped = line.strip()

            if (
                stripped.startswith("- ")
                or stripped.startswith("* ")
                or stripped.startswith("+ ")
            ):
                items.append(stripped[2:].strip())

        return items

    def extract_numbered_lists(
        self,
        section: ParsedSection,
    ) -> List[str]:
        """
        Extract numbered list items.

        Supports:

            1. Item
            2. Item
        """

        items: List[str] = []

        pattern = re.compile(r"^\d+\.\s+(.*)$")

        for line in section.content:

            match = pattern.match(line.strip())

            if match:

                items.append(match.group(1).strip())

        return items

    def extract_tables(
        self,
        section: ParsedSection,
    ) -> List[List[str]]:
        """
        Extract markdown tables.

        Each row is returned as a list of cells.

        Business interpretation belongs to the
        BlueprintCompiler.
        """

        rows: List[List[str]] = []

        for line in section.content:

            stripped = line.strip()

            if "|" not in stripped:
                continue

            # Skip markdown separator rows.
            if (
                set(stripped.replace("|", "").replace("-", "")) == {":"}
                or stripped.replace("|", "").replace("-", "").strip() == ""
            ):
                continue

            cells = [cell.strip() for cell in stripped.split("|")]

            if cells and cells[0] == "":
                cells = cells[1:]

            if cells and cells[-1] == "":
                cells = cells[:-1]

            rows.append(cells)

        return rows

    def extract_code_blocks(
        self,
        section: ParsedSection,
    ) -> List[str]:
        """
        Preserve fenced markdown code blocks.

        The parser stores code exactly as written.
        """

        blocks: List[str] = []

        collecting = False

        buffer: List[str] = []

        for line in section.content:

            stripped = line.rstrip()

            if stripped.startswith("```"):

                if collecting:

                    blocks.append("\n".join(buffer))

                    buffer.clear()

                    collecting = False

                else:

                    collecting = True

                continue

            if collecting:

                buffer.append(line)

        return blocks
        # -----------------------------------------------------

    # Statistics
    # -----------------------------------------------------

    def statistics(
        self,
        document: ParsedDocument,
    ) -> Dict[str, int]:
        """
        Return structural statistics for a parsed document.

        These metrics describe the document structure only and
        intentionally avoid any business interpretation.
        """

        section_count = len(document.sections)

        total_lines = 0
        bullet_items = 0
        numbered_items = 0
        table_rows = 0
        code_blocks = 0

        for section in document.sections:

            total_lines += len(section.content)

            bullet_items += len(self.extract_bullet_lists(section))

            numbered_items += len(self.extract_numbered_lists(section))

            table_rows += len(self.extract_tables(section))

            code_blocks += len(self.extract_code_blocks(section))

        return {
            "sections": section_count,
            "content_lines": total_lines,
            "bullet_items": bullet_items,
            "numbered_items": numbered_items,
            "table_rows": table_rows,
            "code_blocks": code_blocks,
        }

    # -----------------------------------------------------
    # Validation Helpers
    # -----------------------------------------------------

    def is_empty(
        self,
        document: ParsedDocument,
    ) -> bool:
        """
        Determine whether a parsed document contains
        any sections.
        """

        return len(document.sections) == 0

    def has_section(
        self,
        document: ParsedDocument,
        title: str,
    ) -> bool:
        """
        Check whether a section exists.
        """

        return self.find_section(document, title) is not None

    def section_count(
        self,
        document: ParsedDocument,
    ) -> int:
        """
        Return the number of parsed sections.
        """

        return len(document.sections)

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    def diagnostics(
        self,
        document: ParsedDocument,
    ) -> Dict[str, object]:
        """
        Produce parser diagnostics for one document.
        """

        return {
            "filename": document.filename,
            "metadata": document.metadata,
            "statistics": self.statistics(document),
            "section_titles": self.section_titles(document),
        }

    def summary(
        self,
        documents: Dict[str, ParsedDocument],
    ) -> Dict[str, object]:
        """
        Produce an overall parsing summary.
        """

        total_sections = sum(len(doc.sections) for doc in documents.values())

        return {
            "documents": len(documents),
            "sections": total_sections,
            "filenames": sorted(documents.keys()),
        }
        # -----------------------------------------------------

    # Lifecycle
    # -----------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize the Blueprint Parser.

        Reserved for future parser initialization,
        plugin registration and parser configuration.
        """

        self.logger.info("Blueprint Parser initialized.")

    def shutdown(self) -> None:
        """
        Shutdown the Blueprint Parser.
        """

        self.logger.info("Blueprint Parser shutdown completed.")

    # -----------------------------------------------------
    # Parser Information
    # -----------------------------------------------------

    @property
    def version(self) -> str:
        """
        Parser version.
        """

        return "2.0.0"

    @property
    def component_name(self) -> str:
        """
        Component identifier.
        """

        return "Blueprint Parser"

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    def health(self) -> Dict[str, object]:
        """
        Return parser health information.

        Suitable for dashboards, diagnostics and
        factory startup validation.
        """

        return {
            "component": self.component_name,
            "version": self.version,
            "heading_pattern": self.HEADING_PATTERN.pattern,
            "status": "READY",
        }

    # -----------------------------------------------------
    # Utility Methods
    # -----------------------------------------------------

    def supported_elements(self) -> List[str]:
        """
        Return the markdown elements supported by
        the parser.
        """

        return [
            "headings",
            "paragraphs",
            "bullet_lists",
            "numbered_lists",
            "tables",
            "code_blocks",
        ]

    def parser_capabilities(self) -> Dict[str, bool]:
        """
        Describe parser capabilities.

        This allows downstream components to determine
        which markdown constructs are available.
        """

        return {
            "heading_parsing": True,
            "section_parsing": True,
            "bullet_lists": True,
            "numbered_lists": True,
            "tables": True,
            "code_blocks": True,
            "metadata": True,
            "statistics": True,
        }

    # -----------------------------------------------------
    # Representation
    # -----------------------------------------------------

    def __repr__(self) -> str:
        return "BlueprintParser(" f"version='{self.version}')"

    def __str__(self) -> str:
        return f"{self.component_name} " f"[v{self.version}]"
