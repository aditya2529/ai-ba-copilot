# AI BA Copilot — Claude Code Context

## What This App Does
Streamlit app that takes meeting notes / business requirements and generates 2 Jira-ready user stories, with validation, risks, test cases, story point estimation, and Jira push.

## Running the App
```bash
cd D:\Projects\ai-ba-copilot
streamlit run app.py
```

## Critical: File Deployment
Claude Code edits files in the **git worktree** at:
`D:\Projects\ai-ba-copilot\.claude\worktrees\<worktree-name>\`

But the app runs from the **main project directory**:
`D:\Projects\ai-ba-copilot\`

**After every file edit, copy to main directory before testing:**
```bash
cp .claude/worktrees/<worktree>/app.py ./app.py
# repeat for any other edited file
```

## Project Structure
```
app.py                  — Streamlit UI, session state, all button logic
story_generator.py      — generate_user_story() + _normalize_story()
prompts.py              — story_prompt(), validation_prompt(), risk_prompt(), test_case_prompt(), estimation_prompt()
input_validator.py      — validate_input() — cleans/scores meeting notes, extracts Improved Input
jira_mapper.py          — map_to_jira_payload() — parses story text into Jira ADF payload
jira_client.py          — create_jira_issue() — HTTP call to Jira REST API
test_case_generator.py  — extract_valid_stories(), generate_test_cases()
validator.py            — validate_story()
risk_detector.py        — detect_risks()
estimation_engine.py    — estimate_story()
history.py              — load_history(), save_to_history() — JSON-based session history
history.json            — persisted history (max 50 entries, auto-created)
llm_client.py           — call_llm() — wraps Anthropic API call
```

## App Modes
- **Simple (One-click)**: Validate input → Generate story (draft) → Improve story (final) → Validation + Risks + Test Cases + Estimation → optional Jira push. All in one button click.
- **Advanced (Step-by-step)**: Each step is a separate button. User controls the pipeline interactively.

## Key Design Decisions

### Story Normalization
`_normalize_story()` in `story_generator.py` runs on EVERY LLM response before storing in session state. It normalises all LLM output variants (bold titles, "User Story 1:" prefixes, plain titles before Description:) into canonical `Title: / Description: / Acceptance Criteria:` format. This means `extract_valid_stories()` can be simple — it only needs to split on `\nTitle:`.

### Story Generation Flow (Simple Mode)
1. `validate_input(meeting_notes)` → cleans notes, extracts `Improved Input:`
2. `generate_user_story(improved_input)` → first draft using `story_prompt()` (2-story few-shot prompt)
3. Hardened improve prompt → `generate_user_story(improved_input, raw_prompt=True)` → final story
   - **Important**: Step 3 passes `{improved_input}` (cleaned requirements), NOT `{story}` (first draft). Passing the draft caused the LLM to make minimal changes instead of generating fresh high-quality stories.

### `raw_prompt=True` Parameter
`generate_user_story(text, raw_prompt=True)` passes `text` directly to the LLM without wrapping it in `story_prompt()`. Used for improve prompts that already contain the full instructions + few-shot example.

### `extract_valid_stories(text)` — Story Splitting
Splits normalized story text on `\nTitle:`. A chunk is valid if it has `Title:\s*\S` and `Acceptance Criteria:`. Returns at most 2 stories. Jira push aborts if fewer than 1 valid story is found.

### Jira Push Safety
`map_to_jira_payload()` raises `ValueError` if story is missing `Title:` or `Acceptance Criteria:`. Jira push wraps each story in try/except and shows per-story success/error.

### `extract_improved_input(validation_text, fallback="")` Helper
Extracts the `Improved Input:` section from input validation output. Called in 3 places — use this helper, do NOT add inline regex.

### History Sidebar
`history.py` persists up to 50 entries to `history.json`. Sidebar shows past sessions; clicking one restores all session state fields. `save_to_history()` is called after Simple Mode generation and after Advanced Mode Generate/Improve Story.

## Prompt Quality Standard
All story prompts include a few-shot example (library loan story). Quality rules enforced:
- Title: 3–6 words, action-oriented
- Role: specific named persona (not just "user")
- Business value: concrete outcome (not "improve experience")
- 3 ACs per story: happy path / specific failure with exact error message / distinct edge case
- NO bold text, NO "User Story N:" labels, NO extra sections

## Common Bugs to Avoid
- Do NOT call `st.rerun()` after Improve Story buttons — it discards session state writes
- Do NOT clear `st.session_state.validation` after Improve Story — it disables downstream buttons (Risks, Test Cases, Estimate)
- Do NOT pass `{story}` (first draft) to improve prompts — always use `{improved_input}` (cleaned requirements)
- Do NOT add duplicate regex for Improved Input extraction — use `extract_improved_input()`
- Delete `__pycache__` stale `.pyc` files after editing modules if changes aren't reflected

## Environment
- Python + Streamlit
- Anthropic API (Claude) via `llm_client.py`
- Jira REST API via `jira_client.py`
- Secrets stored in Streamlit secrets / `.env` (not committed)
