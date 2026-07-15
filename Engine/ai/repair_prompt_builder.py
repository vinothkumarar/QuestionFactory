"""
Question Factory OS
Repair Prompt Builder
"""


class RepairPromptBuilder:

    def build(self, question, validation):

        prompt = []

        prompt.append("The following generated question failed validation.")

        prompt.append("")

        prompt.append("Validation Errors:")

        for error in validation["errors"]:

            prompt.append(f"- {error}")

        prompt.append("")

        prompt.append("Return ONLY corrected JSON.")

        prompt.append("")

        prompt.append(str(question))

        return "\n".join(prompt)
