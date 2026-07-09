"""
Question Factory OS
Export Engine
"""

from exporters.csv_exporter import CSVExporter


class ExportEngine:

    def __init__(self):

        self.csv_exporter = CSVExporter()

    def export_csv(
        self,
        report,
        output_file="output/questions.csv"
    ):

        self.csv_exporter.export(
            report,
            output_file
        )

        return output_file
        