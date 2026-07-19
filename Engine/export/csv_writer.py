"""
Question Factory OS v2.2

CSV Writer

Responsible for writing CSVRow objects to a UTF-8 CSV file.

This class intentionally performs no validation or mapping.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from Engine.export.constants import (
    CSV_DELIMITER,
    CSV_QUOTECHAR,
)
from Engine.export.models.csv_row import CSVRow
from Engine.export.models.export_options import ExportOptions


class CSVWriter:
    """
    Writes CSVRow objects to disk.
    """

    def write(
        self,
        rows: Iterable[CSVRow],
        options: ExportOptions,
    ) -> Path:
        """
        Write CSV rows to the configured output file.

        Parameters
        ----------
        rows
            CSV rows to export.

        options
            Export configuration.

        Returns
        -------
        Path
            Path of the generated CSV file.
        """

        output_file = options.output_path

        if output_file.exists() and not options.overwrite:
            raise FileExistsError(
                f"File already exists: {output_file}"
            )

        rows = list(rows)

        #
        # Empty export
        #
        if not rows:

            with output_file.open(
                "w",
                encoding=options.encoding,
                newline=options.newline,
            ):
                pass

            return output_file

        fieldnames = rows[0].columns

        with output_file.open(
            mode="w",
            encoding=options.encoding,
            newline=options.newline,
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
                delimiter=CSV_DELIMITER,
                quotechar=CSV_QUOTECHAR,
                quoting=csv.QUOTE_MINIMAL,
                extrasaction="ignore",
            )

            if options.include_header:
                writer.writeheader()

            for row in rows:
                writer.writerow(
                    row.to_dict()
                )

        return output_file

    def append(
        self,
        rows: Iterable[CSVRow],
        options: ExportOptions,
    ) -> Path:
        """
        Append rows to an existing CSV.

        Header is written only if the file does not exist.
        """

        output_file = options.output_path

        rows = list(rows)

        if not rows:
            return output_file

        file_exists = output_file.exists()

        fieldnames = rows[0].columns

        with output_file.open(
            mode="a",
            encoding=options.encoding,
            newline=options.newline,
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
                delimiter=CSV_DELIMITER,
                quotechar=CSV_QUOTECHAR,
                quoting=csv.QUOTE_MINIMAL,
                extrasaction="ignore",
            )

            if (
                options.include_header
                and not file_exists
            ):
                writer.writeheader()

            for row in rows:
                writer.writerow(
                    row.to_dict()
                )

        return output_file

    @staticmethod
    def row_count(
        rows: Iterable[CSVRow],
    ) -> int:
        """
        Return the number of rows.
        """

        return sum(
            1
            for _ in rows
        )
        