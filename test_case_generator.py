from llm_client import call_llm
from prompts import test_case_prompt

def extract_valid_stories(text):
    import re

    if not text:
        return []

    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Story text is already normalized by generate_user_story()/_normalize_story().
    # Just split on newline before Title: and validate each chunk.
    parts = re.split(r"\n(?=Title:)", text)

    stories = []
    for part in parts:
        part = part.strip()
        if not re.search(r"Title:\s*\S", part):
            continue
        if "Acceptance Criteria:" not in part:
            continue
        stories.append(part)

    return stories[:2]


def generate_test_cases(story):
    return call_llm(test_case_prompt(story))