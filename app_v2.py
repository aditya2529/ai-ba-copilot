import streamlit as st
import re
from jira_client import create_jira_issue
from jira_mapper import map_to_jira_payload
from story_generator import generate_user_story
from validator import validate_story
from input_validator import validate_input
from test_case_generator import generate_test_cases

#st.write("Secrets loaded:", st.secrets)
# ---------- CONFIG ----------
st.set_page_config(page_title="AI BA Copilot V2", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.card {
    padding: 18px;
    border-radius: 12px;
    background-color: #1E222A;
    margin-bottom: 15px;
}

.big-btn button {
    height: 3.5em;
    font-size: 16px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Requirement Intelligence Copilot</h1>
<p style='text-align: center; color: gray;'>
From messy notes → clean Jira-ready stories in one click
</p>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
for key in ["story", "validation", "input_validation", "test_cases"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------- STEP 1 ----------
st.markdown("## 📝 Step 1: Enter Requirement")

meeting_notes = st.text_area(
    "",
    height=180,
    placeholder="Example: User should login using OTP..."
)

# ---------- STEP 2 ----------
st.markdown("## ⚡ Step 2: Generate AI Output")

col_center = st.columns([1,2,1])[1]

with col_center:
    if st.button("🚀 Generate Complete Output", key="generate_full"):
        with st.spinner("🤖 AI is working on your requirement..."):

            # FULL PIPELINE
            input_val = validate_input(meeting_notes)
            story = generate_user_story(meeting_notes)
            story_val = validate_story(story)

            st.session_state.input_validation = input_val
            st.session_state.story = story
            st.session_state.validation = story_val

# ---------- OUTPUT ----------
if st.session_state.story:

    st.markdown("## 🤖 AI Output")

    # INPUT QUALITY
    if st.session_state.input_validation:
        st.markdown("### 🧠 Input Analysis")
        st.markdown(f'<div class="card">{st.session_state.input_validation}</div>', unsafe_allow_html=True)

    # STORY
    st.markdown("### 📘 User Story")
    st.markdown(f'<div class="card">{st.session_state.story}</div>', unsafe_allow_html=True)

    # VALIDATION
    if st.session_state.validation:
        st.markdown("### ✅ Story Validation")
        st.markdown(f'<div class="card">{st.session_state.validation}</div>', unsafe_allow_html=True)

    # ---------- ACTIONS ----------
    st.markdown("## ⚙️ Smart Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Improve Story"):
            with st.spinner("Improving..."):
                improved = generate_user_story(
                    st.session_state.story + "\nImprove clarity, structure and acceptance criteria."
                )
                st.session_state.story = improved

    with col2:
        if st.button("🧪 Generate Test Cases"):
            with st.spinner("Generating test cases..."):
                st.session_state.test_cases = generate_test_cases(st.session_state.story)

    with col3:
        if st.button("🚀 Push to Jira"):
            payload = map_to_jira_payload(st.session_state.story)
            response = create_jira_issue(payload)

            if response.status_code == 201:
                st.success(f"✅ Created: {response.json().get('key')}")
            else:
                st.error(response.text)

# ---------- TEST CASE OUTPUT ----------
if st.session_state.test_cases:
    st.markdown("## 🧪 Test Cases")
    st.markdown(f'<div class="card">{st.session_state.test_cases}</div>', unsafe_allow_html=True)