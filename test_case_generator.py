from llm_client import call_llm
from prompts import test_case_prompt

# 🔥 ADD THIS FUNCTION
def split_stories(story_text):
    import re

    # Split on "Title:" and keep delimiter
    parts = re.split(r"(Title:\s*)", story_text)

    stories = []
    current = ""

    for i in range(len(parts)):
        if parts[i].strip() == "Title:":
            if current:
                stories.append(current.strip())
                current = "Title:"
            else:
                current = "Title:"
        else:
            current += parts[i]

    if current:
        stories.append(current.strip())

    # Clean empty
    stories = [s for s in stories if "Title:" in s]

    return stories[:2]


def generate_test_cases(story):
    return call_llm(test_case_prompt(story))