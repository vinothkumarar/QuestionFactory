"""
Question Factory OS
Question Schema Test

Milestone : M7
Sprint    : S1
Release   : R1
"""

from schema.question_schema import QUESTION_COLUMNS
from schema.question_schema import SYSTEM_COLUMNS
from schema.question_schema import EXPORT_COLUMNS

print("=" * 80)
print("QUESTION SCHEMA")
print("=" * 80)

print()

print("Question Columns :", len(QUESTION_COLUMNS))

print("System Columns   :", len(SYSTEM_COLUMNS))

print("Export Columns   :", len(EXPORT_COLUMNS))

print()

print("Export Order")

print("-" * 80)

for index, column in enumerate(EXPORT_COLUMNS, start=1):

    print(f"{index:02d}. {column}")
    