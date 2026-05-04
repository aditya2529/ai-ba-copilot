import re
from llm_client import call_llm
from prompts import story_prompt

def _normalize_story(text):
    """Normalize LLM output to canonical Title:/Description:/Acceptance Criteria: format."""
    if not text:
        return text
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # "**Title Text**" on its own line → "Title: Title Text"
    text = re.sub(r"^\*\*([^*]+?)\*\*[ \t]*$", r"Title: \1", text, flags=re.MULTILINE)
    # Strip any remaining bold markers
    text = re.sub(r"\*\*", "", text)
    # "User Story N: text" → "Title: text"
    text = re.sub(r"User Story\s*\d+\s*:\s*", "Title: ", text)
    # Plain line immediately before "Description:" → "Title: <line>"
    text = re.sub(r"^(?!Title:[ \t])(.+)\n\n?(?=Description:)", r"Title: \1\n\n", text, flags=re.MULTILINE)
    return text.strip()

def generate_user_story(meeting_notes, raw_prompt=False):
    if raw_prompt:
        result = call_llm(meeting_notes)
    else:
        result = call_llm(story_prompt(meeting_notes))
    return _normalize_story(result)