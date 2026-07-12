"""
Question Factory OS
Factory Configuration

Milestone : M8
Sprint    : S1
Release   : R1
"""

# -------------------------------------------------
# Factory Information
# -------------------------------------------------

FACTORY_NAME = "Question Factory OS"

VERSION = "3.1"

OUTPUT_FILE = "output/questions.csv"

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

        "batch_no": 6,

        "question_start": 501,

        "question_count": 20

    }

]
