def story_prompt(notes):
    return f"""
You are a seasoned Lead Business Analyst.
Convert notes into user story.

Title:
Description:
Acceptance Criteria:

Notes:
{notes}
"""

def validation_prompt(story):
    return f"""
Validate the user story.

List issues, score (1-10), and improvements.

Story:
{story}
"""

def risk_prompt(story):
    return f"""
Identify risks, dependencies, and edge cases.

Story:
{story}
"""

def test_case_prompt(story):
    return f"""
Act as a Senior QA Engineer.

Generate test cases strictly based on the user story and acceptance criteria.

STRICT RULES:
- Cover positive, negative, and edge cases
- Each acceptance criteria must have at least one test case
- Include failure scenarios and system behavior validations
- Do NOT miss constraints like retries, limits, validations, or errors

FORMAT (MANDATORY):
Test Case ID:
Title:
Preconditions:
Steps:
Expected Result:

IMPORTANT:
- Ensure test cases are complete and not truncated
- Prioritize critical flows if output length is limited
- Do NOT introduce features not present in the input


User Story:
{story}
"""

def estimation_prompt(story):
    return f"""
You are a senior Agile Business Analyst.

Estimate effort for the following user story.

Provide:

Story Points (Fibonacci scale: 1,2,3,5,8,13)
Reasoning:
- Complexity
- Dependencies
- Unknowns
- Risk factors

Format:

Story Points: <number>

Reasoning:
- ...
- ...
- ...

User Story:
{story}
"""