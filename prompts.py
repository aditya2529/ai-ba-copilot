def story_prompt(notes):
    return f"""You are a Senior Business Analyst.

Generate EXACTLY 2 Jira-ready user stories from the input below.

OUTPUT FORMAT — copy this structure exactly, twice:

Title: <short action-oriented feature name, 3-6 words>

Description:
As a <user>, I want <goal>, so that <business value>.

Acceptance Criteria:
- Given <context>, When <action>, Then <result>
- Given <context>, When <action>, Then <result>
- Given <context>, When <action>, Then <result>

STRICT RULES:
- Output EXACTLY 2 stories — no more, no less
- Every story MUST start with "Title:" on its own line
- NO bold text (**), NO "User Story 1:" or "User Story 2:" labels
- NO extra sections — do not add Risks, Priority, Effort, Assumptions, or Open Questions
- Complete story 1 fully before starting story 2
- Title must NOT start with "As a" or "User Story"
- Exactly 3 Given/When/Then acceptance criteria per story
- Do NOT merge content between stories

Input:
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