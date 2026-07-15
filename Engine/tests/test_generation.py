"""
Question Factory OS
End-to-End Generation Test
"""

from builders.question_builder import QuestionBuilder
from ai.prompt_builder import PromptBuilder
from ai.provider_factory import ProviderFactory

runtime = {
    "current_project": "P1",
    "current_chapter": "CH1",
    "current_subtopic": "ST4",
    "current_set": "S1",
}


# Build Question Skeleton
question = QuestionBuilder().build(runtime, 1)

print("=" * 80)
print("QUESTION CODE")
print("=" * 80)
print(question["question_code"])

# Build Prompt
prompt = PromptBuilder().build(question)

print("=" * 80)
print("PROMPT LENGTH")
print("=" * 80)
print(len(prompt))

# Generate
provider = ProviderFactory.create()

print("=" * 80)
print("GENERATING...")
print("=" * 80)

response = provider.generate(prompt)
from ai.response_parser import ResponseParser
from builders.question_merger import QuestionMerger

parser = ResponseParser()

ai_data = parser.parse(response)

merged = QuestionMerger().merge(question, ai_data)

print("=" * 80)
print("MERGED QUESTION")
print("=" * 80)

for key, value in merged.items():
    print(f"{key}: {value}")

print("=" * 80)
print("RAW RESPONSE")
print("=" * 80)
print(response)
