from llm_client import call_llm
from prompts import risk_prompt

def detect_risks(story):
    return call_llm(risk_prompt(story))