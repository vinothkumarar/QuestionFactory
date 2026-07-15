"""
Question Factory OS
Factory Configuration

Milestone : M13
Sprint    : S1
Release   : R1
"""

# -------------------------------------------------
# Factory Information
# -------------------------------------------------

FACTORY_NAME = "Question Factory OS"

VERSION = "3.2"

OUTPUT_FILE = "output/questions.csv"

# -------------------------------------------------
# Retry Configuration
# -------------------------------------------------

MAX_RETRY_COUNT = 3

RETRY_DELAY_SECONDS = 2

# -------------------------------------------------
# Production Orders
# -------------------------------------------------

PRODUCTION_ORDERS = [
    {
        "order_id": "ORDER_001",
        "subject": "Physics",
        "unit": "P1",
        "chapter": "CH1",
        "subtopic": "ST4",
        "set_no": "S1",
        "batch_no": 8,
        "question_start": 701,
        "question_count": 100,
    }
]
