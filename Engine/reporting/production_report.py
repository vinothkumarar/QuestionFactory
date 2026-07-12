"""
Question Factory OS
Production Report

Milestone : M12
Sprint    : S5
Release   : R1
"""


class ProductionReport:

    def print_report(

        self,

        request,

        batch_result,

        validation_result,

        csv_file

    ):

        print()

        print("=" * 80)
        print("PRODUCTION QUALITY REPORT")
        print("=" * 80)

        print()

        print(f"Production Order    : {request.request_id}")
        print(f"Subject             : {request.subject}")
        print(f"Unit                : {request.unit}")
        print(f"Chapter             : {request.chapter}")
        print(f"Subtopic            : {request.subtopic}")
        print(f"Set                 : {request.set_no}")

        print()

        print("-" * 80)

        print(f"Questions Requested : {request.total_questions}")

        print(f"Questions Generated : {batch_result.successful}")

        print(f"Validation Passed   : {batch_result.successful}")

        print(f"Validation Failed   : {batch_result.failed}")

        success_rate = (

            batch_result.successful

            / request.total_questions

        ) * 100

        print(

            f"Success Rate        : "

            f"{success_rate:.2f}%"

        )

        print()

        avg_time = (

            batch_result.execution_time_ms

            / max(batch_result.successful, 1)

        )

        print(

            f"Average Time        : "

            f"{avg_time:.0f} ms/question"

        )

        print()

        print(

            f"CSV Export          : {csv_file}"

        )

        print(

            f"CSV Validation      : "

            f"{'PASS' if validation_result.passed else 'FAIL'}"

        )

        print()

        if validation_result.passed:

            print(

                "Overall Status      : READY FOR SUPABASE IMPORT"

            )

        else:

            print(

                "Overall Status      : VALIDATION FAILED"

            )

        print()

        print("=" * 80)
        