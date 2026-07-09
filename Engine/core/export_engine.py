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
        runtime: dict
    ):

        return self.csv_exporter.export(
            report,
            runtime
        )
            