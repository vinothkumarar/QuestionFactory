"""
Question Factory OS
CSV Exporter
"""

import csv
from pathlib import Path


class CSVExporter:

    def export(self, report, output_file):

        output_path = Path(output_file)

        rows = []

        for result in report.results:

            rows.append(
                result["question"]
            )

        if not rows:
            return

        fieldnames = list(rows[0].keys())

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                extrasaction="ignore"
            )

            writer.writeheader()

            writer.writerows(rows)

        print()

        print("=" * 80)
        print("CSV EXPORTED")
        print("=" * 80)

        print(output_path.resolve())
        