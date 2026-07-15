from core.resource_manager import ResourceManager
from core.csv_writer import CSVWriter

resource_manager = ResourceManager()

folder = resource_manager.ensure_questionbank_path("P1", "CH1", "ST4")

writer = CSVWriter()

csv_file = writer.create_batch_file(folder, "P1_CH1_ST4_S1_B1.csv")

print(csv_file)
