"""
Question Factory OS v3.0

Rule Engine
"""

from __future__ import annotations

from Engine.models.generated_question_model import GeneratedQuestionModel
from Engine.quality.quality_report import QualityReport

from Engine.quality.option_validator import OptionValidator
from Engine.quality.difficulty_validator import DifficultyValidator
from Engine.quality.archetype_validator import ArchetypeValidator
from Engine.quality.semantic_validator import SemanticValidator
from Engine.quality.duplicate_detector import DuplicateDetector


class RuleEngine:
    """
    Executes all quality validation rules.
    """

    def validate(
        self,
        question: GeneratedQuestionModel,
    ) -> QualityReport:
        """
        Execute all quality validators.
        """

        report = QualityReport()

        # -----------------------------------------------------
        # Option Validation
        # -----------------------------------------------------

        option_report = OptionValidator().validate(question)

        for error in option_report.errors:
            report.add_error(error)

        for warning in option_report.warnings:
            report.add_warning(warning)

        for recommendation in option_report.recommendations:
            report.add_recommendation(recommendation)

        # -----------------------------------------------------
        # Difficulty Validation
        # -----------------------------------------------------

        difficulty_report = DifficultyValidator().validate(question)

        for error in difficulty_report.errors:
            report.add_error(error)

        for warning in difficulty_report.warnings:
            report.add_warning(warning)

        for recommendation in difficulty_report.recommendations:
            report.add_recommendation(recommendation)

        # -----------------------------------------------------
        # Archetype Validation
        # -----------------------------------------------------

        archetype_report = ArchetypeValidator().validate(question)

        for error in archetype_report.errors:
            report.add_error(error)

        for warning in archetype_report.warnings:
            report.add_warning(warning)

        for recommendation in archetype_report.recommendations:
            report.add_recommendation(recommendation)
        
        # -----------------------------------------------------
        # Semantic Validation
        # -----------------------------------------------------

        semantic_report = SemanticValidator().validate(question)

        for error in semantic_report.errors:
            report.add_error(error)

        for warning in semantic_report.warnings:
            report.add_warning(warning)

        for recommendation in semantic_report.recommendations:
            report.add_recommendation(recommendation)

        # -----------------------------------------------------
        # Duplicate Detection
        # -----------------------------------------------------

        duplicate_report = DuplicateDetector().validate(question)

        for error in duplicate_report.errors:
            report.add_error(error)

        for warning in duplicate_report.warnings:
            report.add_warning(warning)

        for recommendation in duplicate_report.recommendations:
            report.add_recommendation(recommendation)

        report.calculate_score()

        return report
        