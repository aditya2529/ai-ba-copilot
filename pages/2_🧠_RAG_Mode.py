"""RAG Mode — Org-aware story generation.

Same end-to-end pipeline as Simple Mode in app.py, but augments the story
prompt with similar past stories retrieved from a local vector store.
"""

import re
import streamlit as st

from input_validator import validate_input
from story_generator import generate_user_story
from validator import validate_story
from risk_detector import detect_risks
from test_case_generator import generate_test_cases, extract_valid_stories
from estimation_engine import estimate_story
from jira_client import create_jira_issue
from jira_mapper import map_to_jira_payload
from history import save_to_history

from rag import ingest as rag_ingest
from rag import retriever as rag_retriever
from rag import store as rag_store


st.set_page_config(page_title="RAG Mode — AI BA Copilot", layout="wide")


# ─── HELPERS ──────────────────────────────────────────────────────────────

def extract_improved_input(validation_text, fallback=""):
    m = re.search(r"Improved Input:\s*\n(.+)", validation_text or "", re.DOTALL)
    return m.group(1).strip() if m else fallback


def _render_corpus_status():
    try:
        counts = rag_store.count()
    except Exception as e:
        st.error(f"Corpus unavailable: {e}")
        return None
    total = counts.get("total", 0)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Total", total)
    c2.metric("🕐 From History", counts.get("history", 0))
    c3.metric("📁 From Uploads", counts.get("upload", 0))
    c4.metric("🎫 From Jira", counts.get("jira", 0))
    return counts


# ─── SESSION STATE ────────────────────────────────────────────────────────

for key in [
    "rag_input_validation", "rag_story", "rag_validation",
    "rag_risks", "rag_test_cases", "rag_estimation",
    "rag_retrieved_preview", "rag_flash",
]:
    if key not in st.session_state:
        st.session_state[key] = None


# ─── HEADER ───────────────────────────────────────────────────────────────

st.markdown("""
<h1 style='text-align:center;'>🧠 RAG Mode</h1>
<p style='text-align:center; color: gray;'>Stories that sound like <i>your team</i> wrote them.</p>
""", unsafe_allow_html=True)

st.info(
    "Beta — this page uses Retrieval-Augmented Generation. It learns from "
    "your past stories, uploaded BRDs/PRDs, and Jira history, then writes "
    "new stories in your team's voice. The main Simple/Advanced modes "
    "are unaffected."
)

# ─── CORPUS STATUS ────────────────────────────────────────────────────────

st.markdown("### 📊 Corpus Status")
counts = _render_corpus_status()

# Show any flash message carried over from the last ingest (after rerun)
if st.session_state.get("rag_flash"):
    st.success(st.session_state.rag_flash)
    st.session_state.rag_flash = None

# ─── CORPUS MANAGEMENT ────────────────────────────────────────────────────

with st.expander("⚙️ Manage Corpus (add sources)", expanded=(counts is not None and counts.get("total", 0) == 0)):
    tab_h, tab_u, tab_j = st.tabs(["🕐 History", "📁 Upload BRD / PRD", "🎫 Jira Import"])

    with tab_h:
        st.caption("Re-index every story in your local history.json.")
        if st.button("🔄 Re-ingest history.json", key="rag_ingest_history"):
            with st.spinner("Indexing history..."):
                try:
                    added = rag_ingest.ingest_history()
                    st.session_state.rag_flash = f"✅ Added {added} new entries from history."
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {e}")

    with tab_u:
        st.caption("Drop in PDFs or DOCX files. Text is extracted, chunked, embedded.")
        uploads = st.file_uploader(
            "Upload one or more files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="rag_uploader",
        )
        if uploads and st.button("📥 Ingest Uploads", key="rag_ingest_uploads"):
            total_added = 0
            errors = []
            with st.spinner("Extracting and embedding..."):
                for f in uploads:
                    added, err = rag_ingest.ingest_file(f.name, f.read())
                    total_added += added
                    if err:
                        errors.append(err)
            for err in errors:
                st.warning(err)
            if total_added:
                st.session_state.rag_flash = f"✅ Indexed {total_added} chunks from {len(uploads)} file(s)."
                st.rerun()

    with tab_j:
        st.caption("Pulls every Story-type issue from your configured Jira project.")
        max_n = st.number_input("Max issues to import (0 = all)", min_value=0, value=0, step=10, key="rag_jira_max")
        if st.button("🎫 Pull past stories from Jira", key="rag_ingest_jira"):
            with st.spinner("Fetching from Jira..."):
                added, err = rag_ingest.ingest_jira(max_results=(max_n or None))
            if err:
                st.error(f"Failed: {err}")
            else:
                st.session_state.rag_flash = f"✅ Indexed {added} new Jira stories."
                st.rerun()


# ─── INPUT ────────────────────────────────────────────────────────────────

st.markdown("### 📝 Input")
meeting_notes = st.text_area("Paste meeting notes or requirements", key="rag_meeting_notes", height=180)

# Match-strictness control: lower threshold = only very-similar stories are used.
strictness = st.slider(
    "🎚️ Match strictness — how similar a past story must be to be used as context",
    min_value=0.30, max_value=1.00, value=0.65, step=0.05,
    help="Lower = stricter (only near-identical past stories qualify). "
         "Higher = looser (more, but weaker, matches get used). 0.65 is a good default.",
    key="rag_strictness",
)
st.caption(
    "Strict (≤0.50): only near-identical past stories shape the output.  ·  "
    "Balanced (0.65): related stories.  ·  Loose (≥0.80): almost anything matches."
)

# Live retrieval preview (before user clicks Generate)
if meeting_notes and meeting_notes.strip():
    with st.expander("🔍 Top similar past items from your corpus (preview)", expanded=True):
        try:
            all_matches = rag_retriever.retrieve_all(meeting_notes, k=3)
        except Exception as e:
            st.warning(f"Retrieval failed: {e}")
            all_matches = []
        if not all_matches:
            st.caption("No matches yet. Add sources above to start building your corpus.")
        else:
            passing = [m for m in all_matches if (m.get("distance") is None or m["distance"] <= strictness)]
            st.caption(f"✅ {len(passing)} of {len(all_matches)} matches qualify at strictness {strictness:.2f} — only these shape the output.")
            for i, m in enumerate(all_matches, start=1):
                meta = m.get("metadata") or {}
                src = meta.get("source", "?")
                label = meta.get("label", "")
                dist = m.get("distance")
                qualifies = dist is None or dist <= strictness
                badge = "🟢 USED" if qualifies else "⚪ skipped (too weak)"
                st.markdown(
                    f"**Example {i}** — `{src}` · {label}  ·  distance: `{dist:.3f}`  ·  {badge}"
                    if dist is not None else
                    f"**Example {i}** — `{src}` · {label}  ·  {badge}"
                )
                st.code((m.get("text") or "")[:600] + ("..." if len(m.get("text") or "") > 600 else ""))


# ─── GENERATE ─────────────────────────────────────────────────────────────

if st.button("🚀 Generate (RAG-augmented)", key="rag_generate_btn"):
    if not meeting_notes.strip():
        st.warning("Please enter input first.")
    else:
        # 1. Input validation
        with st.spinner("🔍 Validating input..."):
            input_validation = validate_input(meeting_notes)
        improved_input = extract_improved_input(input_validation, fallback=meeting_notes)
        st.session_state.rag_input_validation = input_validation

        with st.expander("✨ Improved Input (AI Cleaned)"):
            st.code(improved_input)

        # 2. Retrieve context (respecting the strictness slider)
        with st.spinner("🧠 Retrieving similar past stories..."):
            try:
                context = rag_retriever.retrieve_context(improved_input, k=3, max_distance=strictness)
            except Exception as e:
                st.warning(f"Retrieval failed, falling back to non-RAG: {e}")
                context = ""
        st.session_state.rag_retrieved_preview = context

        if context:
            st.success(f"📚 Retrieved org context (strictness {strictness:.2f}) — generating in your team's voice.")
        else:
            st.info(f"ℹ️ No matches strong enough at strictness {strictness:.2f} — generating without RAG context. Try raising the slider.")

        # 3a. Generate first draft (with RAG context) — same as Simple Mode step 3
        with st.spinner("✍️ Generating first draft..."):
            draft = generate_user_story(improved_input, similar_stories=context or None)

        # 3b. Improve pass — same hardened prompt as Simple Mode, with org context
        #     injected so BOTH passes stay in your team's voice.
        org_context_block = ""
        if context:
            org_context_block = f"""
--- SIMILAR PAST STORIES FROM YOUR ORG (match this terminology and style) ---

{context}

--- END SIMILAR PAST STORIES ---
"""
        improved_prompt = f"""
You are a Senior Business Analyst with 10 years of enterprise Agile experience.

Generate EXACTLY 2 production-ready Jira stories from the requirements at the bottom.
Use the EXAMPLE below as your quality benchmark — match its level of specificity.
{org_context_block}
--- EXAMPLE OF A HIGH-QUALITY STORY ---

Title: Extend Book Loan Before Due Date

Description:
As a registered library member, I want to extend my book loan online before the due date, so that I avoid late fees without needing to visit the library in person.

Acceptance Criteria:
- Given a member has an active loan with 3 or more days remaining, When they click "Extend Loan" on the My Loans page, Then the due date is extended by 14 days and a confirmation email is sent to the member within 2 minutes.
- Given a member has already extended the same loan once, When they attempt to click "Extend Loan" again, Then the system displays the message "Maximum extensions reached — please return or renew in person" and the Extend button is disabled.
- Given a member has an outstanding fine greater than $5.00, When they navigate to the My Loans page, Then all Extend Loan buttons are greyed out and a banner reads "Clear your outstanding balance to re-enable loan extensions."

--- END EXAMPLE ---

QUALITY RULES:
- Title: 3–6 words, specific and action-oriented. BAD: "Improve Checkout". GOOD: "Validate Card Fields on Submission"
- Role: a specific named persona. BAD: "user", "customer/user". GOOD: "registered customer", "guest shopper"
- Business value: concrete outcome. BAD: "improve experience". GOOD: "prevent failed payments from invalid card data"
- Each AC must cover a DIFFERENT scenario — no two ACs test the same thing
- Each AC must name the exact UI element, field name, error message, or system state
- AC 1 = success/happy path with specific outcome
- AC 2 = specific failure with exact error message or UI state
- AC 3 = distinct edge case — NOT a repeat of AC 2

STRICT FORMAT RULES:
- Output EXACTLY 2 stories
- Every story starts with "Title:" on its own line
- NO bold text (**), NO "User Story 1/2:" labels
- NO extra sections (Risks, Assumptions, Notes, Priority)
- Complete story 1 fully before starting story 2
- One workflow per story — do NOT merge features

Requirements to convert into 2 production-ready user stories:
{improved_input}
"""
        with st.spinner("✨ Improving stories (your team's voice)..."):
            story = generate_user_story(improved_prompt, raw_prompt=True)
        st.session_state.rag_story = story

        # 4. Full downstream pipeline
        with st.spinner("⚙️ Running validation, risks, tests, estimation..."):
            st.session_state.rag_validation = validate_story(story)
            st.session_state.rag_risks = detect_risks(story)
            st.session_state.rag_test_cases = generate_test_cases(story)
            st.session_state.rag_estimation = estimate_story(story)

        # 5. Save to history (auto-feeds back into corpus via history.py hook)
        save_to_history(
            mode="RAG",
            meeting_notes=meeting_notes,
            story=story,
            validation=st.session_state.rag_validation,
            risks=st.session_state.rag_risks,
            test_cases=st.session_state.rag_test_cases,
            estimation=st.session_state.rag_estimation,
        )

        st.success("✅ Done. Scroll down for outputs.")


# ─── OUTPUT PREVIEW ───────────────────────────────────────────────────────

st.markdown("### 📊 Output Preview")
if st.session_state.rag_story:
    st.code(st.session_state.rag_story, language=None)
else:
    st.info("👉 Generated story will appear here.")


# ─── TABS ─────────────────────────────────────────────────────────────────

tab_ctx, tab_story, tab_val, tab_risk, tab_test, tab_est = st.tabs(
    ["📚 Retrieved Context", "🧾 Story", "✅ Validation", "⚠️ Risks", "🧪 Test Cases", "📊 Estimation"]
)

with tab_ctx:
    if st.session_state.rag_retrieved_preview:
        st.code(st.session_state.rag_retrieved_preview)
    else:
        st.caption("No context retrieved (yet).")

with tab_story:
    if st.session_state.rag_story:
        st.code(st.session_state.rag_story)
        st.markdown("### 🚀 Push to Jira")
        if st.button("🚀 Push Clean Story to Jira", key="rag_push_jira"):
            stories = extract_valid_stories(st.session_state.rag_story)
            if len(stories) < 1:
                st.error("❌ No valid stories extracted.")
            else:
                for s in stories:
                    try:
                        payload = map_to_jira_payload(s)
                        response = create_jira_issue(payload)
                        if response.status_code == 201:
                            st.success(f"✅ Created: {response.json().get('key')}")
                            # Approved by push → feed this story into the AI's memory
                            try:
                                rag_ingest.add_pushed_story(s, mode="RAG")
                            except Exception:
                                pass
                        else:
                            st.error(response.text)
                    except ValueError as e:
                        st.error(f"⚠️ Skipped: {e}")

with tab_val:
    if st.session_state.rag_validation:
        st.code(st.session_state.rag_validation)

with tab_risk:
    if st.session_state.rag_risks:
        st.code(st.session_state.rag_risks)

with tab_test:
    if st.session_state.rag_test_cases:
        st.markdown(st.session_state.rag_test_cases)

with tab_est:
    if st.session_state.rag_estimation:
        st.markdown(st.session_state.rag_estimation)
