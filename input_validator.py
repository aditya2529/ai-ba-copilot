from llm_client import call_llm

def validate_input(meeting_notes):
    prompt = f"""
You are a Senior Business Analyst working in an enterprise Agile environment.

Your task is to evaluate the quality of raw meeting notes before they are used to generate user stories.

Analyze the input for clarity, completeness, and structure.

Meeting Notes:
\"\"\"
{meeting_notes}
\"\"\"

Evaluate the following:

1. Actor (Who is performing the action?)
2. Action (What needs to be done?)
3. Business Goal (Why is this needed?)

Also check for:
- Ambiguity or vague language
- Missing details
- Unclear requirements
- Lack of context

Instructions:

- Do NOT reject the input
- Be constructive and helpful
- ONLY clean and restructure the input — do NOT generate user stories

Respond STRICTLY in this format — do not deviate:

Score: X/10

Issues:
- <issue 1>
- <issue 2>
- ...

Suggestions:
- <suggestion 1>
- <suggestion 2>
- ...

Improved Input:
<Rewrite the meeting notes as clear, structured requirements. Do NOT write user stories or acceptance criteria here.>
"""

    return call_llm(prompt)