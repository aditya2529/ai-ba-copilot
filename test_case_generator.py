from llm_client import call_llm
from prompts import test_case_prompt

def generate_test_cases(story):
    return call_llm(test_case_prompt(story))