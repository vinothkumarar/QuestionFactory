"""
Question Factory OS
Question Merger Test
"""

from builders.question_builder import QuestionBuilder
from builders.question_merger import QuestionMerger

runtime = {
    "current_project": "P1",
    "current_chapter": "CH1",
    "current_subtopic": "ST4",
    "current_set": "S1",
    "current_batch": 6,
}

builder = QuestionBuilder()

skeleton = builder.build(runtime, 501)

ai_question = {
    "difficulty": "Foundation",
    "difficulty_score": 1,
    "question_text": "What is the SI unit of length?",
    "option_a": "metre",
    "option_b": "second",
    "option_c": "kilogram",
    "option_d": "ampere",
    "correct_option": "A",
    "answer": "The SI unit of length is metre.",
    "explanation": "Length is a base physical quantity.",
    "tags": ["SI Units", "Length"],
}

merger = QuestionMerger()

question = merger.merge(skeleton, ai_question)

print("=" * 80)
print("QUESTION CODE")
print("=" * 80)

print(question["question_code"])

print()

print("=" * 80)
print("QUESTION TEXT")
print("=" * 80)

print(question["question_text"])

print()

print("=" * 80)
print("DIFFICULTY")
print("=" * 80)

print(question["difficulty"])

print()

print("=" * 80)
print("MARKS")
print("=" * 80)

print(question["marks"])

print()

print("=" * 80)
print("BATCH")
print("=" * 80)

print(question["batch_no"])
