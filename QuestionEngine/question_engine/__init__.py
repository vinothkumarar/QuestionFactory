"""Independent dual question engine foundation."""

from .curriculum import CurriculumLoader, CurriculumSnapshot
from .export import QuestionCSVExporter
from .generation import GenerationRequest, QuestionGenerationProvider
from .models import QuestionCandidate, QuestionOrigin, QuestionQualityScores
from .quality import QuestionQualityGate
from .pyq_registry import PYQSourceRegistry
from .pdf_ingest import PDFTextExtractor, PDFExtractionResult, PDFPageText
from .verification import AnswerVerificationResult, QuestionAnswerVerifier
from .scope_verification import ScopeVerificationResult, QuestionScopeVerifier
from .pyq_segmenter import PYQTextSegmenter, PYQTextFragment, PYQSegmentationResult
from .openai_provider import OpenAIQuestionGenerationProvider, OpenAIProviderError

__all__ = [
    "CurriculumLoader",
    "CurriculumSnapshot",
    "QuestionCandidate",
    "QuestionCSVExporter",
    "GenerationRequest",
    "QuestionGenerationProvider",
    "QuestionOrigin",
    "QuestionQualityScores",
    "QuestionQualityGate",
    "PYQSourceRegistry",
    "PDFTextExtractor",
    "PDFExtractionResult",
    "PDFPageText",
    "AnswerVerificationResult",
    "QuestionAnswerVerifier",
    "ScopeVerificationResult",
    "QuestionScopeVerifier",
    "PYQTextSegmenter",
    "PYQTextFragment",
    "PYQSegmentationResult",
    "OpenAIQuestionGenerationProvider",
    "OpenAIProviderError",
]
