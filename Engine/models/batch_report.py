"""
Question Factory OS
Batch Report
"""


class BatchReport:

    def __init__(self):

        self.total = 0

        self.passed = 0

        self.failed = 0

        self.results = []

    def add_result(
        self,
        question,
        validation
    ):

        self.total += 1

        if validation["passed"]:
            self.passed += 1
        else:
            self.failed += 1

        self.results.append({

            "question": question,

            "validation": validation

        })

    def summary(self):

        success_rate = 0

        if self.total > 0:

            success_rate = (
                self.passed / self.total
            ) * 100

        return {

            "total": self.total,

            "passed": self.passed,

            "failed": self.failed,

            "success_rate": round(
                success_rate,
                2
            )

        }
        