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
# ---------- INPUT ----------
st.markdown("### 📝 Input")
meeting_notes = st.text_area("Paste meeting notes or Business Requirements", key="meeting_notes", height=200)





# ---------- ACTIONS ----------
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

            # 🔥 ADD THESE LINES
           # st.session_state.story_generated = True
            
            # st.session_state.story_validated = False

with c3:
    if st.button("✅ Validate Story", disabled=not st.session_state.story):
        st.session_state.validation = validate_story(st.session_state.story)

        # 🔥 ADD THIS
        st.session_state.story_validated = True

with c4:
    if st.button("🔄 Improve Story", disabled=not st.session_state.validation):
        with st.spinner("Improving story..."):
            improved_prompt = st.session_state.story + "\n\nImprove clarity, structure and acceptance criteria."
            st.session_state.story = generate_user_story(improved_prompt)

with c5:
    if st.button("⚠️ Risks", disabled=not st.session_state.validation):
        st.session_state.risks = detect_risks(st.session_state.story)

with c6:
    if st.button("🧪 Test Cases", disabled=not st.session_state.validation):
        st.session_state.test_cases = generate_test_cases(st.session_state.story)

# 👇 ADD THIS EXTRA (for estimate)
if st.button("📊 Estimate", disabled=not st.session_state.validation):
    st.session_state.estimation = estimate_story(st.session_state.story)


# ---------- SMART GUIDANCE ----------

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