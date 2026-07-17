"""
Question Factory OS
Database Engine
"""

from Engine.database.supabase_adapter import (
    SupabaseAdapter,
)


class DatabaseEngine:

    def __init__(self):

        self.adapter = SupabaseAdapter()

    def save_question(self, question):

        return self.adapter.insert_question(question)

    def save_batch(self, report):

        inserted = 0

        skipped = 0

        for result in report.results:

            success = self.save_question(result["question"])

            if success:

                inserted += 1

            else:

                skipped += 1

        return {"inserted": inserted, "skipped": skipped}
