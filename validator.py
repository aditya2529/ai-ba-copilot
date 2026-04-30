from llm_client import call_llm
from prompts import validation_prompt

def validate_story(story):
    return call_llm(validation_prompt(story))