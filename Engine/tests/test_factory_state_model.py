"""
Question Factory OS
Factory State Model Test
"""

from models.factory_state_model import FactoryStateModel

factory_state = FactoryStateModel(
    project="P1", chapter="CH1", subtopic="ST4", set_no="S1", current_batch=3
)

print("=" * 80)
print("FACTORY STATE")
print("=" * 80)

print(factory_state)
