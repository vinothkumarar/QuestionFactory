"""Independent dual question engine foundation."""

from .curriculum import CurriculumLoader, CurriculumSnapshot
from .concept_catalog import ConceptCatalog, ConceptCatalogError, ConceptEntry
from .export import QuestionCSVExporter
from .generation import GenerationRequest, QuestionGenerationProvider
from .models import QuestionCandidate, QuestionOrigin, QuestionQualityScores
from .quality import QuestionQualityGate
from .pyq_registry import PYQSourceRegistry
from .pdf_ingest import PDFTextExtractor, PDFExtractionResult, PDFPageText
from .verification import (
    AnswerVerificationResult, QuestionAnswerVerifier, IntegerArithmeticExpressionVerifier,
)
from .scope_verification import (
    ScopeVerificationResult, QuestionScopeVerifier, ApprovedCatalogScopeVerifier,
)
from .pyq_segmenter import PYQTextSegmenter, PYQTextFragment, PYQSegmentationResult
from .openai_provider import OpenAIQuestionGenerationProvider, OpenAIProviderError
from .exam_syllabus import (
    ExamSyllabusRegistry, ExamSyllabusRegistryError, ExamSyllabusSource,
    ExamSyllabusMapping, ExamVersionedQuestionScopeVerifier,
)

__all__ = [
    "CurriculumLoader", "CurriculumSnapshot", "ConceptCatalog",
    "ConceptCatalogError", "ConceptEntry", "QuestionCandidate",
    "QuestionCSVExporter", "GenerationRequest", "QuestionGenerationProvider",
    "QuestionOrigin", "QuestionQualityScores", "QuestionQualityGate",
    "PYQSourceRegistry", "PDFTextExtractor", "PDFExtractionResult",
    "PDFPageText", "AnswerVerificationResult", "QuestionAnswerVerifier",
    "IntegerArithmeticExpressionVerifier", "ScopeVerificationResult",
    "QuestionScopeVerifier", "ApprovedCatalogScopeVerifier",
    "PYQTextSegmenter", "PYQTextFragment", "PYQSegmentationResult",
    "OpenAIQuestionGenerationProvider", "OpenAIProviderError",
    "ExamSyllabusRegistry", "ExamSyllabusRegistryError",
    "ExamSyllabusSource", "ExamSyllabusMapping",
    "ExamVersionedQuestionScopeVerifier",
]
