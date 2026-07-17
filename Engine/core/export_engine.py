"""
Question Factory OS
Export Engine
"""

from Engine.exporters.csv_exporter import CSVExporter


class ExportEngine:
    def __init__(self) -> None:
        self.csv_exporter = CSVExporter()

    def export_csv(self, report, runtime: dict):
        return self.csv_exporter.export(report, runtime)
        