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

Generate structured test cases strictly based on the user stories and acceptance criteria.

STRICTLY FOLLOW the format below. If the format is not followed, the answer is incorrect.

STRICT RULES:

1. Generate EXACTLY 6 test cases

2. Test cases MUST include:
- 2 positive (happy path)
- 2 negative (validation/failure)
- 2 edge cases

3. Each test case MUST follow this format:

Test Case ID: TC_<number>

Title: <Short descriptive title>

Steps:
1. <Step 1>
2. <Step 2>
3. <Step 3>

Expected Result:
<Clear system behavior outcome>

4. COVERAGE RULES:
- Test cases must align with acceptance criteria
- Include system validations, failures, retries, and constraints
- Do NOT miss critical scenarios like duplicate actions, invalid input, or system inconsistency

5. DO NOT:
- Write vague steps
- Skip steps
- Combine multiple scenarios in one test case
- Add explanations outside the format

6. IMPORTANT:
- Keep output concise, structured, and complete
- Do NOT exceed 6 test cases
- Do NOT truncate any test case
- Do NOT introduce features not present in the input

User Stories:
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