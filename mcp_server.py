"""AI BA Copilot — MCP Server (Phase 3 MVP)

Exposes the BA Copilot pipeline as Model Context Protocol tools so that ANY
MCP-compatible AI agent (Claude Desktop, your agent platform, etc.) can call
it to turn meeting notes into Jira-ready stories — no human button-clicking.

Run it:
    pip install "mcp[cli]"
    python mcp_server.py            # stdio transport (for Claude Desktop)

Register in Claude Desktop (claude_desktop_config.json):
    {
      "mcpServers": {
        "ai-ba-copilot": {
          "command": "python",
          "args": ["D:\\\\Projects\\\\ai-ba-copilot\\\\mcp_server.py"],
          "env": {
            "GROQ_API_KEY": "your-groq-key",
            "JIRA_EMAIL": "you@example.com",
            "JIRA_API_TOKEN": "your-jira-token"
          }
        }
      }
    }

Jira credentials come from environment variables (JIRA_EMAIL / JIRA_API_TOKEN)
since there is no Streamlit runtime here — see jira_client._get_jira_credentials.
"""

from mcp.server.fastmcp import FastMCP

from story_generator import generate_user_story
from validator import validate_story as _validate_story
from risk_detector import detect_risks as _detect_risks
from test_case_generator import generate_test_cases as _generate_test_cases
from test_case_generator import extract_valid_stories
from estimation_engine import estimate_story as _estimate_story
from input_validator import validate_input as _validate_input
from jira_client import create_jira_issue
from jira_mapper import map_to_jira_payload

mcp = FastMCP("ai-ba-copilot")


@mcp.tool()
def validate_input(meeting_notes: str) -> str:
    """Score and clean raw meeting notes before story generation.

    Returns a quality score, issues, suggestions, and a cleaned 'Improved
    Input' version of the notes.
    """
    return _validate_input(meeting_notes)


@mcp.tool()
def generate_story(meeting_notes: str, use_rag: bool = False) -> str:
    """Turn meeting notes / requirements into EXACTLY 2 Jira-ready user stories.

    Each story has a Title, a Description (As a / I want / So that), and 3
    Given-When-Then acceptance criteria.

    Set use_rag=True to bias the output toward your organisation's existing
    stories (retrieved from the local vector store). Requires the corpus to be
    populated; falls back to standard generation if retrieval fails or finds
    nothing.
    """
    context = None
    if use_rag:
        try:
            from rag.retriever import retrieve_context
            context = retrieve_context(meeting_notes, k=3) or None
        except Exception:
            context = None
    return generate_user_story(meeting_notes, similar_stories=context)


@mcp.tool()
def validate_story(story: str) -> str:
    """Review a user story for quality. Returns issues, a 1-10 score, and
    suggested improvements."""
    return _validate_story(story)


@mcp.tool()
def detect_risks(story: str) -> str:
    """Identify risks, dependencies, and edge cases for a user story."""
    return _detect_risks(story)


@mcp.tool()
def generate_test_cases(story: str) -> str:
    """Generate 6 structured test cases (2 happy, 2 negative, 2 edge) for a
    user story."""
    return _generate_test_cases(story)


@mcp.tool()
def estimate_story(story: str) -> str:
    """Estimate effort in Fibonacci story points (1,2,3,5,8,13) with reasoning."""
    return _estimate_story(story)


@mcp.tool()
def push_to_jira(story: str) -> str:
    """Push user stories to Jira as separate Story issues.

    Accepts the canonical Title/Description/Acceptance Criteria format (the
    output of generate_story). Returns a summary of created issue keys or
    per-story errors.
    """
    stories = extract_valid_stories(story)
    if not stories:
        return "No valid stories found to push (need Title + Acceptance Criteria sections)."

    results = []
    for i, s in enumerate(stories, start=1):
        try:
            payload = map_to_jira_payload(s)
            response = create_jira_issue(payload)
            if response.status_code == 201:
                key = response.json().get("key")
                results.append(f"Story {i}: created {key}")
            else:
                results.append(f"Story {i}: failed ({response.status_code}) {response.text[:150]}")
        except Exception as e:
            results.append(f"Story {i}: error — {e}")

    return "\n".join(results)


@mcp.tool()
def full_pipeline(meeting_notes: str, use_rag: bool = False, push: bool = False) -> str:
    """End-to-end: notes -> validate -> generate -> validate -> risks -> tests
    -> estimate, optionally pushing to Jira.

    Returns a single combined report. Set push=True to also create Jira issues.
    """
    cleaned = _validate_input(meeting_notes)
    story = generate_story(meeting_notes, use_rag=use_rag)
    validation = _validate_story(story)
    risks = _detect_risks(story)
    tests = _generate_test_cases(story)
    estimation = _estimate_story(story)

    sections = [
        "=== INPUT VALIDATION ===\n" + cleaned,
        "=== STORIES ===\n" + story,
        "=== STORY VALIDATION ===\n" + validation,
        "=== RISKS ===\n" + risks,
        "=== TEST CASES ===\n" + tests,
        "=== ESTIMATION ===\n" + estimation,
    ]
    if push:
        sections.append("=== JIRA PUSH ===\n" + push_to_jira(story))

    return "\n\n".join(sections)


if __name__ == "__main__":
    mcp.run()
