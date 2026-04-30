from llm_client import call_llm
from prompts import story_prompt

def generate_user_story(meeting_notes):
    prompt = f"""
    You are a senior Business Analyst.

    Convert meeting notes into a structured user story.

    Format:
    Title:
    Description:
    Acceptance Criteria:

    Notes:
    {meeting_notes}
    """

    return call_llm(story_prompt(meeting_notes))