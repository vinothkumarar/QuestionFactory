"""
Question Factory OS
CSV Validator Test

Milestone : M7
Sprint    : S3
Release   : R1
"""

from validators.csv_validator import CSVValidator

validator = CSVValidator()

result = validator.validate("output/questions.csv")

print("=" * 80)
print("CSV VALIDATOR")
print("=" * 80)

print()

print("Rows Checked :", result.total_rows)

print("Passed       :", result.passed)

print("Errors       :", result.total_errors)

if result.errors:

    print()

    print("Validation Errors")

    print("-" * 80)

    for error in result.errors:

        print(error)
