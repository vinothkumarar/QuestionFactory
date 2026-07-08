"""
Question Factory OS
Prompt Builder

Builds prompts for AI providers.
"""


class PromptBuilder:

    def build(self, question: dict) -> str:

        return f"""
Generate one high-quality JEE question.

Subject:
{question.get('subject_name')}

Unit:
{question.get('unit_name')}

Chapter:
{question.get('chapter_name')}

Subtopic:
{question.get('subtopic_name')}

Return:
- Question
- Four options
- Correct answer
- Detailed explanation
""".strip()
