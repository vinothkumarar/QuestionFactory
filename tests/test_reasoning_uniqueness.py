"""Offline regression tests for subtopic reasoning-uniqueness review."""
import json
import unittest
from types import SimpleNamespace
from Engine.integration.reasoning_uniqueness import review_reasoning_uniqueness, question_skeleton


class FakeResponses:
    def __init__(self, duplicate=False):
        self.calls = []
        self.duplicate = duplicate

    def create(self, *, model, input):
        self.calls.append(input)
        data = json.loads(input.split("\n")[1])
        ids = [x["id"] for x in data]
        duplicates = []
        if self.duplicate and "existing_0" in ids:
            duplicates = [{"new_id": "new_0", "matches_id": "existing_0",
                           "reason": "same solution structure"}]
        return SimpleNamespace(output_text=json.dumps({"duplicates": duplicates}))


class UniquenessTests(unittest.TestCase):
    def test_numeric_changes_same_skeleton(self):
        self.assertEqual(question_skeleton("A price rises 20%."),
                         question_skeleton("A price rises 35%."))

    def test_chunking_covers_entire_subtopic_bank(self):
        fake = FakeResponses()
        existing = [{"question_text": "Distinct example " + str(i) + " with pattern " + str(i*i)}
                    for i in range(85)]
        result = review_reasoning_uniqueness(SimpleNamespace(responses=fake),
                   [{"question_text": "Find the final value after an increase."}],
                   existing, chunk_size=40)
        self.assertEqual(result["chunks_reviewed"], 3)
        self.assertEqual(result["existing_count"], 85)
        self.assertEqual(len(fake.calls), 3)

    def test_reasoning_duplicate_rejected(self):
        fake = FakeResponses(duplicate=True)
        with self.assertRaisesRegex(RuntimeError, "Reasoning-equivalent"):
            review_reasoning_uniqueness(SimpleNamespace(responses=fake),
                 [{"question_text": "What is the selling price?"}],
                 [{"question_text": "Calculate the final selling price."}])

    def test_same_structure_different_numbers_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Repeated question structure"):
            review_reasoning_uniqueness(SimpleNamespace(responses=FakeResponses()),
                 [{"question_text": "Find 20 percent of 150."}],
                 [{"question_text": "Find 30 percent of 250."}])


if __name__ == "__main__":
    unittest.main()
