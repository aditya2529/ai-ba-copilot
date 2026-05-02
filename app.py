import streamlit as st
import json
import re
from jira_client import create_jira_issue
from jira_mapper import map_to_jira_payload
from story_generator import generate_user_story
from validator import validate_story
from risk_detector import detect_risks
from test_case_generator import generate_test_cases
from estimation_engine import estimate_story
from input_validator import validate_input

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI BA Copilot", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1E222A;
}
</style>
""", unsafe_allow_html=True)



# ---------- SESSION STATE ----------
for key in ["input_validation","input_score","story","validation","risks","test_cases","estimation"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "story_generated" not in st.session_state:
    st.session_state.story_generated = False

if "story_validated" not in st.session_state:
    st.session_state.story_validated = False

if "meeting_notes" not in st.session_state:
    st.session_state.meeting_notes = ""

# ---------- APPLY IMPROVED INPUT ----------
if "apply_improved" in st.session_state and st.session_state.apply_improved:
    st.session_state.meeting_notes = st.session_state.apply_improved
    st.session_state.apply_improved = None

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Requirement Intelligence Copilot</h1>
<p style='text-align: center; color: gray;'>
From messy notes → production-ready Jira stories
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; max-width: 800px; margin: 10px auto; color: #A0A0A0; font-size: 15px; line-height: 1.6;'>

Transform your raw meeting notes into structured user stories, acceptance criteria, and test cases in seconds.  
Follow the guided steps below to validate your input, generate a high-quality story, and push it directly to Jira.

</div>
""", unsafe_allow_html=True)

# ---------- ONE CLICK PIPELINE ----------
def run_full_pipeline(input_text):
    result = {}

    validation = validate_input(input_text)
    result["input_validation"] = validation
    #improved_input = input_text
    # 🔥 Extract improved input from validation
    improved_match = re.search(r"Improved Input:\n(.+)", validation, re.DOTALL)
    if improved_match:
     improved_input = improved_match.group(1).strip()
    else:
     improved_input = input_text

    story = generate_user_story(improved_input)

    validation_story = validate_story(story)
    risks = detect_risks(story)
    test_cases = generate_test_cases(story)
    estimation = estimate_story(story)

    result["story"] = story
    result["validation"] = validation_story
    result["risks"] = risks
    result["test_cases"] = test_cases
    result["estimation"] = estimation

    return result

mode = st.radio(
    "Choose Mode",
    ["Simple (One-click)", "Advanced (Step-by-step)"]
)
if mode == "Simple (One-click)":
    st.info("⚡ Simple Mode: Generate everything (User Story, Validation, Risks, Test Cases, Estimation) in one click. Ideal for quick results.")

elif mode == "Advanced (Step-by-step)":
    st.info("⚙️ Advanced Mode: Execute each step individually (Validate → Generate → Improve → Risks → Test Cases → Estimation). Ideal for detailed control and refinement.")


# ---------- INPUT ----------
st.markdown("### 📝 Input")
meeting_notes = st.text_area("Paste meeting notes or Business Requirements", key="meeting_notes", height=200)



if mode == "Simple (One-click)":

    st.markdown("### ⚡ One Click Execution")

    auto_push = st.checkbox("🚀 Auto push to Jira (only if satisfied with output)")

    if st.button("🚀 Generate Everything", key="generate_all_btn"):

        if not meeting_notes.strip():
            st.warning("Please enter input first")

        else:
            # 🔍 Step 1: Validate input
            with st.spinner("🔍 Analyzing input..."):
                validation = validate_input(meeting_notes)

            # 🔍 Step 2: Extract improved input
            improved_match = re.search(r"Improved Input:\n(.+)", validation, re.DOTALL)

            if improved_match:
                improved_input = improved_match.group(1).strip()
            else:
                improved_input = meeting_notes
                # 👇 ADD RIGHT HERE
            st.info("ℹ️ Your input was automatically refined to improve clarity before generating the story.")

            with st.expander("✨ Improved Input (AI Cleaned)"):
                st.code(improved_input)

            # 🧠 Step 3: Generate story
            with st.spinner("🧠 Generating user story..."):
                story = generate_user_story(improved_input)

            # ✨ Step 4: Improve story
            improved_prompt = f"""
Act as a Senior Business Analyst.

Refine the user story into production-ready Jira format.

STRICT RULES:
- Each story must be independent
- Use THIS structure ONLY:

Title:
As a [user],
I want [goal],
So that [business value]

Acceptance Criteria (MANDATORY Given-When-Then):
- At least 5 criteria
- Must be testable and specific
- Include success + failure + edge cases

Include:
- Edge Cases
- Assumptions
- Open Questions (if ambiguity exists)

DO NOT:
- Be generic
- Combine multiple features into one story
- Leave incomplete sections

IMPORTANT:
- Identify ALL distinct workflows from the input (e.g., validation, approval, notification, logging)
- Create at least ONE user story per workflow (combine only if strongly related)
- Do NOT miss any requirement from the input
- Cover success, failure, and edge-case scenarios for each workflow
- Include constraints like retries, limits, validations, and system behaviors where mentioned
- Do NOT introduce features not present in the input
- If output length is limited, reduce verbosity but still cover all workflows
- Prefer concise acceptance criteria over verbose descriptions
- If content is too large, generate only the first 2–3 complete user stories
- Do NOT truncate any story mid-way
- Ensure ALL explicit actions mentioned in input (e.g., cancel, audit, approve, reject) are converted into user stories

User Story:
{story}
"""
            final_story = generate_user_story(improved_prompt)

            # ⚙️ Step 5: Remaining pipeline
            with st.spinner("⚙️ Running validations, risks, and test cases..."):
                validation_story = validate_story(final_story)
                risks = detect_risks(final_story)
                test_cases = generate_test_cases(final_story)
                estimation = estimate_story(final_story)

            # 📦 Step 6: Output
            output = {
                "input_validation": validation,
                "story": final_story,
                "validation": validation_story,
                "risks": risks,
                "test_cases": test_cases,
                "estimation": estimation
            }

            # ✅ SAVE TO SESSION (IMPORTANT)
            st.session_state.input_validation = output["input_validation"]
            st.session_state.story = output["story"]
            st.session_state.validation = output["validation"]
            st.session_state.risks = output["risks"]
            st.session_state.test_cases = output["test_cases"]
            st.session_state.estimation = output["estimation"]

            # 🚀 OPTIONAL JIRA PUSH
            if auto_push:
                payload = map_to_jira_payload(final_story)
                response = create_jira_issue(payload)

                if response.status_code == 201:
                    st.success(f"✅ Jira Created: {response.json().get('key')}")
                else:
                    st.error(response.text)

            # ✅ SUCCESS MESSAGE
            st.success("✅ Input processed successfully")

            # 📊 SCORE
            score_match = re.search(r'(\d+)/10', validation)
            score = score_match.group(1) if score_match else "7"
            st.metric("📊 Input Quality Score", f"{score}/10")

            # 🔍 VALIDATION VIEW
            with st.expander("🔍 View Input Validation"):
                st.code(validation)
# ---------- ACTIONS ----------
if mode == "Advanced (Step-by-step)":
    st.markdown("### ⚙️ Actions")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        if st.button("🧠 Validate Input"):
            result = validate_input(meeting_notes)
            st.session_state.input_validation = result

            score_match = re.search(r'(\d+)/10', result)
            st.session_state.input_score = int(score_match.group(1)) if score_match else 7

    with c2:
        if st.button("🧾 Generate", disabled=not st.session_state.input_validation):
            with st.spinner("Generating..."):
                st.session_state.story = generate_user_story(meeting_notes)

    with c3:
        if st.button("✅ Validate Story", disabled=not st.session_state.story):
            st.session_state.validation = validate_story(st.session_state.story)
            st.session_state.story_validated = True

    with c4:
        if st.button("🔄 Improve Story", disabled=not st.session_state.validation):
            with st.spinner("Improving story..."):
                #improved_prompt = st.session_state.story + "\n\nImprove clarity, structure and acceptance criteria."
                improved_prompt = f"""
Refine the following user story for:
- clarity
- proper structure
- INVEST principles
- strong acceptance criteria

User Story:
{st.session_state.story}
"""
                st.session_state.story = generate_user_story(improved_prompt)

    with c5:
        if st.button("⚠️ Risks", disabled=not st.session_state.validation):
            st.session_state.risks = detect_risks(st.session_state.story)

    with c6:
        if st.button("🧪 Test Cases", disabled=not st.session_state.validation):
            st.session_state.test_cases = generate_test_cases(st.session_state.story)

    if st.button("📊 Estimate", disabled=not st.session_state.validation):
        st.session_state.estimation = estimate_story(st.session_state.story)

# ---------- SMART GUIDANCE ----------

# ---------- SMART GUIDANCE ----------

if mode == "Advanced (Step-by-step)":

    if not st.session_state.input_validation:
        st.info("👉 Step 1: Click 'Validate Input and use the improved input'")

    elif st.session_state.story is None:
        st.info("👉 Step 2: Click 'Generate Story'")

    elif st.session_state.validation is None:
        st.info("👉 Step 3: Click 'Validate Story'")

    elif st.session_state.validation and st.session_state.risks is None:
        st.info("👉 Step 4: Improve Story OR Review Risks")

    else:
        st.success("👉 Final Step: Generate Test Cases / Estimate / Push to Jira from Story section 🚀")
# ---------- OUTPUT PREVIEW ----------
st.markdown("### 📊 Output Preview of User Story")

if st.session_state.get("story"):
    st.markdown(f"""
    <div class="card">{st.session_state.story}</div>
    """, unsafe_allow_html=True)
else:
    st.info("👉 Generated story will appear here instantly")

# ---------- TABS ----------
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧠 Input", "🧾 Story", "✅ Validation", "⚠️ Risks", "🧪 Test Cases", "📊 Estimation"]
)

# ---------- INPUT VALIDATION ----------
with tab0:
    if st.session_state.input_validation:
        st.code(st.session_state.input_validation)

        improved_match = re.search(r"Improved Input:\n(.+)", st.session_state.input_validation, re.DOTALL)

        if improved_match:
            improved_input = improved_match.group(1).strip()

            st.markdown("### ✨ Suggested Improved Input")
            st.markdown(f'<div class="card">{improved_input}</div>', unsafe_allow_html=True)

            if st.button("🚀 Use Improved Input"):
                st.session_state.apply_improved = improved_input
                st.rerun()

# ---------- STORY + JIRA ----------
with tab1:
    if st.session_state.story:
        st.code(st.session_state.story)

        st.markdown("### 🚀 Push to Jira")

        if st.button("🚀 Push Clean Story to Jira", disabled=not st.session_state.validation):
            payload = map_to_jira_payload(st.session_state.story)
            response = create_jira_issue(payload)

            if response.status_code == 201:
                st.success(f"✅ Created: {response.json().get('key')}")
            else:
                st.error(response.text)

# ---------- VALIDATION ----------
with tab2:
    if st.session_state.validation:
        st.code(st.session_state.validation)

# ---------- RISKS ----------
with tab3:
    if st.session_state.risks:
        st.code(st.session_state.risks)

# ---------- TEST CASES ----------
with tab4:
    if st.session_state.test_cases:
        st.markdown(st.session_state.test_cases)

# ---------- ESTIMATION ----------
with tab5:
    if st.session_state.estimation:
        st.markdown(st.session_state.estimation)


def generate_all_stories(input_text):

    stories = []

    # ---------- CALL 1 ----------
    prompt1 = f"""
Generate 2 high-priority user stories from the input.

Input:
{input_text}
"""
    raw1 = generate_user_story(prompt1)

    # 🔥 USE YOUR ORIGINAL IMPROVE PROMPT
    improved_prompt1 = f"""
Act as a Senior Business Analyst.

Refine the user story into production-ready Jira format.

STRICT RULES:
- Each story must be independent
- Use THIS structure ONLY:

Title:
As a [user],
I want [goal],
So that [business value]

Acceptance Criteria (MANDATORY Given-When-Then):
- At least 5 criteria
- Must be testable and specific
- Include success + failure + edge cases

Include:
- Edge Cases
- Assumptions
- Open Questions (if ambiguity exists)

DO NOT:
- Be generic
- Combine multiple features into one story
- Leave incomplete sections

IMPORTANT:
- Identify ALL distinct workflows from the input
- Create at least ONE user story per workflow
- Do NOT miss any requirement
- Cover success, failure, and edge cases
- Do NOT introduce features not present in input
- Do NOT truncate any story

User Story:
{raw1}
"""
    improved1 = generate_user_story(improved_prompt1)
    stories.append(improved1)

    # ---------- CALL 2 ----------
    prompt2 = f"""
Generate remaining user stories NOT already covered.

Input:
{input_text}

Already covered:
{improved1}
"""
    raw2 = generate_user_story(prompt2)

    # 🔥 SAME IMPROVE PROMPT AGAIN
    improved_prompt2 = improved_prompt1.replace(raw1, raw2)

    improved2 = generate_user_story(improved_prompt2)
    stories.append(improved2)

    return "\n\n".join(stories)

def generate_all_test_cases(stories):

    test_cases = []

    # ---------- CALL 1 ----------
    prompt1 = f"""
Act as a Senior QA Engineer.

Generate test cases for the MOST CRITICAL user stories.

STRICT RULES:
- Cover positive, negative, and edge cases
- Each acceptance criteria must have at least one test case
- Include failure scenarios
- Do NOT truncate

FORMAT:
Test Case ID:
Title:
Preconditions:
Steps:
Expected Result:

User Stories:
{stories}
"""
    tc1 = generate_test_cases(prompt1)

    # ---------- CALL 2 ----------
    prompt2 = f"""
Generate remaining test cases NOT already covered.

STRICT:
- Do NOT repeat previous test cases
- Focus on uncovered stories or scenarios
- Do NOT truncate

Already Generated:
{tc1}

User Stories:
{stories}
"""
    tc2 = generate_test_cases(prompt2)

    test_cases.append(tc1)
    test_cases.append(tc2)

    return "\n\n".join(test_cases)