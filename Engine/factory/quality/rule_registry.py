"""
Question Factory OS v3.0

Quality Rule Registry

Frozen validation rule definitions.
"""

from __future__ import annotations

from Engine.factory.quality.models.validation_rule import (
    ValidationRule,
)

from Engine.factory.quality.models.validation_severity import (
    ValidationSeverity,
)

QA001 = ValidationRule(
    rule_id="QA001",
    name="Question Count",
    description="Batch contains the expected number of questions.",
    severity=ValidationSeverity.CRITICAL,
)

QA002 = ValidationRule(
    rule_id="QA002",
    name="Question Text",
    description="Every question must contain text.",
    severity=ValidationSeverity.CRITICAL,
)

QA003 = ValidationRule(
    rule_id="QA003",
    name="Option Count",
    description="Every question must contain exactly four options.",
    severity=ValidationSeverity.CRITICAL,
)

QA004 = ValidationRule(
    rule_id="QA004",
    name="Unique Options",
    description="Options must be unique.",
    severity=ValidationSeverity.CRITICAL,
)

QA005 = ValidationRule(
    rule_id="QA005",
    name="Correct Answer",
    description="Every question must have one valid correct answer.",
    severity=ValidationSeverity.CRITICAL,
)

QA006 = ValidationRule(
    rule_id="QA006",
    name="Explanation",
    description="Every question should include an explanation.",
    severity=ValidationSeverity.ERROR,
)

QA007 = ValidationRule(
    rule_id="QA007",
    name="Difficulty",
    description="Difficulty must match the production blueprint.",
    severity=ValidationSeverity.ERROR,
)

QA008 = ValidationRule(
    rule_id="QA008",
    name="Archetype",
    description="Question archetype must be valid.",
    severity=ValidationSeverity.ERROR,
)

QA009 = ValidationRule(
    rule_id="QA009",
    name="Bloom Level",
    description="Bloom taxonomy level should be specified.",
    severity=ValidationSeverity.WARNING,
)

QA010 = ValidationRule(
    rule_id="QA010",
    name="Blueprint Compliance",
    description="Question must comply with the blueprint.",
    severity=ValidationSeverity.ERROR,
)

QA011 = ValidationRule(
    rule_id="QA011",
    name="Duplicate Question",
    description="Question must not duplicate another question.",
    severity=ValidationSeverity.CRITICAL,
)

QA012 = ValidationRule(
    rule_id="QA012",
    name="CSV Compatibility",
    description="Question must be exportable to CSV.",
    severity=ValidationSeverity.CRITICAL,
)

QA013 = ValidationRule(
    rule_id="QA013",
    name="Metadata",
    description="Required metadata must be present.",
    severity=ValidationSeverity.ERROR,
)

QA014 = ValidationRule(
    rule_id="QA014",
    name="Internal Consistency",
    description="Question data must be internally consistent.",
    severity=ValidationSeverity.CRITICAL,
)

ALL_RULES: tuple[ValidationRule, ...] = (
    QA001,
    QA002,
    QA003,
    QA004,
    QA005,
    QA006,
    QA007,
    QA008,
    QA009,
    QA010,
    QA011,
    QA012,
    QA013,
    QA014,
)

__all__ = [
    "QA001",
    "QA002",
    "QA003",
    "QA004",
    "QA005",
    "QA006",
    "QA007",
    "QA008",
    "QA009",
    "QA010",
    "QA011",
    "QA012",
    "QA013",
    "QA014",
    "ALL_RULES",
]
