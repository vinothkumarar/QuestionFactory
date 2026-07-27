"""
Question Factory OS
Factory State Model Test
"""

from Engine.models.factory_state_model import FactoryStateModel

factory_state = FactoryStateModel(
    subject="Physics",
    unit="P1",
    chapter="CH1",
    subtopic="ST1",
    set_no="S1",
    current_batch=1,
)

print("=" * 80)
print("FACTORY STATE")
print("=" * 80)

print(factory_state)
