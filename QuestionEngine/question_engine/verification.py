"""Independent answer-verification contract and conservative integer verifier."""

from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass
from typing import Callable, Protocol

from .models import QuestionCandidate


@dataclass(frozen=True)
class AnswerVerificationResult:
    question_id: str
    verified: bool
    method: str
    evidence: str
    reason: str = ""


class QuestionAnswerVerifier(Protocol):
    """A verifier independent of the question-generation provider."""

    def verify(self, question: QuestionCandidate) -> AnswerVerificationResult:
        """Check the answer and reasoning; return traceable evidence."""
        ...


class IntegerArithmeticExpressionVerifier:
    """Verify only 'Evaluate: <integer expression>' single-correct MCQs.

    This deliberately narrow verifier does not use eval/exec. Unsupported
    formats remain unverified for a broader independent review.
    """

    METHOD = "deterministic-integer-expression-v1"
    PREFIX = re.compile(r"^\s*Evaluate\s*:\s*(.*?)\s*[?.]?\s*$", re.IGNORECASE)
    MAX_EXPRESSION_LENGTH = 120
    MAX_ABS_VALUE = 10**12
    MAX_AST_NODES = 40
    BINARY_OPERATORS: dict[type[ast.operator], Callable[[int, int], int]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }
    UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[int], int]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def verify(self, question: QuestionCandidate) -> AnswerVerificationResult:
        def reject(reason: str) -> AnswerVerificationResult:
            return AnswerVerificationResult(
                question.question_id, False, self.METHOD, "", reason
            )

        if question.answer_type.upper() != "SINGLE_CORRECT":
            return reject("Unsupported answer type; only SINGLE_CORRECT is supported")
        match = self.PREFIX.fullmatch(question.question_text)
        if not match or not match.group(1).strip():
            return reject("Unsupported question format; expected 'Evaluate: <integer expression>'")
        expression = match.group(1).strip()
        if len(expression) > self.MAX_EXPRESSION_LENGTH:
            return reject("Expression exceeds the supported length limit")
        try:
            tree = ast.parse(expression, mode="eval")
            if sum(1 for _ in ast.walk(tree)) > self.MAX_AST_NODES:
                return reject("Expression exceeds the supported complexity limit")
            result = self._evaluate_node(tree.body)
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            return reject("Expression could not be safely verified")

        if len(question.options) != 4:
            return reject("Exactly four answer options are required")
        option_values = [self._parse_integer(option) for option in question.options]
        if any(value is None for value in option_values):
            return reject("All four options must be plain integer values")
        values = [int(value) for value in option_values if value is not None]
        if len(set(values)) != 4:
            return reject("Options must have four distinct integer values")
        if values.count(result) != 1:
            return reject("The independently computed result does not match exactly one option")
        supplied = self._parse_integer(question.correct_answer)
        if supplied is None:
            return reject("Correct answer must be expressed as an integer value")
        if supplied != result:
            return reject(
                f"Supplied answer {supplied} disagrees with independently computed result {result}"
            )
        evidence = (
            f"Restricted expression '{expression}' independently evaluated to {result}; "
            "exactly one of four distinct integer options matches, and the supplied "
            "correct answer matches the computed result."
        )
        return AnswerVerificationResult(
            question.question_id, True, self.METHOD, evidence
        )

    def _evaluate_node(self, node: ast.AST) -> int:
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return self._bounded(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.UNARY_OPERATORS:
            value = self._evaluate_node(node.operand)
            return self._bounded(self.UNARY_OPERATORS[type(node.op)](value))
        if isinstance(node, ast.BinOp) and type(node.op) in self.BINARY_OPERATORS:
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return self._bounded(self.BINARY_OPERATORS[type(node.op)](left, right))
        raise ValueError("Unsupported expression syntax or operator")

    def _bounded(self, value: int) -> int:
        if abs(value) > self.MAX_ABS_VALUE:
            raise ValueError("Intermediate result exceeds supported range")
        return value

    @staticmethod
    def _parse_integer(value: str) -> int | None:
        candidate = value.strip()
        if not re.fullmatch(r"[+-]?\d+", candidate):
            return None
        try:
            return int(candidate)
        except ValueError:
            return None



class DivisibilityRuleVerifier:
    """Verify a narrowly defined 'Which integers is divisible by N?' MCQ.

    This is a deterministic rule checker, not a general number-theory solver.
    """

    METHOD = "deterministic-integer-divisibility-v1"
    QUESTION_PATTERN = re.compile(
        r"^\\s*Which (?:of these|of the following) integers is divisible by (\\d+)\\?\\s*$",
        re.IGNORECASE,
    )
    MAX_DIVISOR = 10**6
    MAX_OPTION_VALUE = 10**12

    def verify(self, question: QuestionCandidate) -> AnswerVerificationResult:
        def reject(reason: str) -> AnswerVerificationResult:
            return AnswerVerificationResult(
                question.question_id, False, self.METHOD, "", reason
            )

        if question.answer_type.upper() != "SINGLE_CORRECT":
            return reject("Unsupported answer type; only SINGLE_CORRECT is supported")
        match = self.QUESTION_PATTERN.fullmatch(question.question_text)
        if not match:
            return reject(
                "Unsupported question format; expected "
                "'Which of these integers is divisible by N?'"
            )
        divisor = int(match.group(1))
        if divisor < 2 or divisor > self.MAX_DIVISOR:
            return reject("Divisor must be between 2 and the supported maximum")
        if len(question.options) != 4:
            return reject("Exactly four answer options are required")
        values = [self._parse_integer(option) for option in question.options]
        if any(value is None for value in values):
            return reject("All four options must be plain integer values")
        integers = [int(value) for value in values if value is not None]
        if len(set(integers)) != 4:
            return reject("Options must have four distinct integer values")
        if any(abs(value) > self.MAX_OPTION_VALUE for value in integers):
            return reject("An option exceeds the supported integer range")
        matching = [value for value in integers if value % divisor == 0]
        if len(matching) != 1:
            return reject(
                "Exactly one option must be divisible by the stated divisor; "
                f"found {len(matching)}"
            )
        supplied = self._parse_integer(question.correct_answer)
        if supplied is None:
            return reject("Correct answer must be expressed as an integer value")
        if supplied != matching[0]:
            return reject(
                f"Supplied answer {supplied} disagrees with independently "
                f"verified divisible option {matching[0]}"
            )
        evidence = (
            f"Checked each of four distinct integer options modulo {divisor}; "
            f"exactly one option ({matching[0]}) has remainder zero and the "
            "supplied correct answer matches."
        )
        return AnswerVerificationResult(
            question.question_id, True, self.METHOD, evidence
        )

    @staticmethod
    def _parse_integer(value: str) -> int | None:
        candidate = value.strip()
        if not re.fullmatch(r"[+-]?\\d+", candidate):
            return None
        try:
            return int(candidate)
        except ValueError:
            return None
