"""
Question Factory OS
Factory State Manager Test
"""

from models.factory_state_model import FactoryStateModel
from core.factory_state_manager import FactoryStateManager


state = FactoryStateModel(

    project="P1",

    chapter="CH1",

    subtopic="ST4",

    set_no="S1",

    current_batch=3

)

manager = FactoryStateManager()

print("=" * 80)
print("FACTORY STATE")
print("=" * 80)
print(state)

print()

print("=" * 80)
print("QUESTION RANGE")
print("=" * 80)

print("Start :", manager.get_question_start(state))
print("End   :", manager.get_question_end(state))

print()

print("=" * 80)
print("NEXT BATCH")
print("=" * 80)

print(manager.get_next_batch(state))

print()

print("=" * 80)
print("ADVANCE BATCH")
print("=" * 80)

state = manager.advance_batch(state)

print(state)

print()

print("=" * 80)
print("NEW QUESTION RANGE")
print("=" * 80)

print("Start :", manager.get_question_start(state))
print("End   :", manager.get_question_end(state))
