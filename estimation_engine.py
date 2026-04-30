from llm_client import call_llm
from prompts import estimation_prompt

def estimate_story(story):
    return call_llm(estimation_prompt(story))