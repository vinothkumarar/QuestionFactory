"""
Question Factory OS
Factory Configuration Test

Milestone : M8
Sprint    : S1
Release   : R1
"""

from config.factory_config import FACTORY_NAME
from config.factory_config import VERSION
from config.factory_config import OUTPUT_FILE
from config.factory_config import PRODUCTION_ORDERS

print("=" * 80)
print("FACTORY CONFIGURATION")
print("=" * 80)

print()

print("Factory Name :", FACTORY_NAME)

print("Version      :", VERSION)

print("Output File  :", OUTPUT_FILE)

print()

print("Production Orders")

print("-" * 80)

for order in PRODUCTION_ORDERS:

    print(order)
