def story_prompt(notes):
    return f"""You are a Senior Business Analyst with 10 years of enterprise Agile experience.

Generate EXACTLY 2 Jira-ready user stories from the Input section at the bottom.

--- EXAMPLE OF A HIGH-QUALITY STORY (follow this standard exactly) ---

Title: Extend Book Loan Before Due Date

Description:
As a registered library member, I want to extend my book loan online before the due date, so that I avoid late fees without needing to visit the library in person.

Acceptance Criteria:
- Given a member has an active loan with 3 or more days remaining, When they click "Extend Loan" on the My Loans page, Then the due date is extended by 14 days and a confirmation email is sent to the member within 2 minutes.
- Given a member has already extended the same loan once, When they attempt to click "Extend Loan" again, Then the system displays the message "Maximum extensions reached — please return or renew in person" and the Extend button is disabled.
- Given a member has an outstanding fine greater than $5.00, When they navigate to the My Loans page, Then all Extend Loan buttons are greyed out and a banner reads "Clear your outstanding balance to re-enable loan extensions."

--- END EXAMPLE ---

QUALITY RULES — apply to every story you write:
- Title: 3–6 words, specific and action-oriented. BAD: "Improve Checkout". GOOD: "Validate Card Fields on Submission"
- Role: a specific named persona. BAD: "user", "customer/user". GOOD: "registered customer", "guest shopper", "admin"
- Business value: concrete outcome, not a feeling. BAD: "improve experience". GOOD: "prevent payment failures from invalid card data"
- Each AC must cover a DIFFERENT scenario — no two ACs test the same thing
- Each AC must name the exact UI element, field, message text, or system behaviour — no vague phrases like "an error is shown" or "it works correctly"
- AC 1 = happy path with specific success outcome
- AC 2 = specific failure/validation with exact error message or UI state
- AC 3 = a distinct edge case (not a repeat of AC 2 with different wording)

STRICT FORMAT RULES:
- Output EXACTLY 2 stories — no more, no less
- Every story MUST start with "Title:" on its own line
- NO bold text (**), NO "User Story 1:" or "User Story 2:" labels
- NO extra sections (Risks, Priority, Effort, Assumptions, Notes)
- Complete story 1 fully before starting story 2
- Each story covers ONE workflow only — do NOT merge two features into one story

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