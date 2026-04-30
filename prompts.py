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
You are a QA expert.

Generate test cases in Zephyr (Jira) format.

Each test case should include:

Test Case ID:
Title:
Preconditions:
Steps:
Expected Result:

Create:
- Positive test cases
- Negative test cases
- Edge cases

Format clearly and consistently.

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