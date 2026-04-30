import os
import ollama
from dotenv import load_dotenv
#from openai import OpenAI

# Load API key
load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 🔹 Generic LLM Call
#import ollama

def call_llm(prompt):
    response = ollama.chat(
        model='phi3',
        messages=[
            {'role': 'system', 'content': 'You are a senior Business Analyst.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']


# 🔹 1. Story Generator
def generate_user_story(meeting_notes):
    prompt = f"""
    You are a senior Business Analyst with strong experience in writing clear, testable user stories.

    Convert the meeting notes into a high-quality user story.

    Follow STRICT structure:

    Title:
    - Short and clear

    Description:
    - As a <user>, I want <goal>, so that <benefit>

    Acceptance Criteria:
    - Use bullet points
    - Include edge cases
    - Ensure testability
    - Cover success and failure scenarios

    Important:
    - Do not be vague
    - Add missing logical details if needed
    - Think like a QA + BA

    Meeting Notes:
    {meeting_notes}
    """

    return call_llm(prompt)


# 🔹 2. Validation Engine
# def validate_story(story):
    prompt = f"""
    Validate the following user story.

    Check:
    - Ambiguity
    - Missing acceptance criteria
    - Testability issues

    Output:
    - Issues (bullet points)
    - Quality Score (1-10)
    - Suggestions

    Story:
    {story}
    """
    return call_llm(prompt)


# 🔹 3. Risk Detection (🔥 key feature)
#def detect_risks(story):
    prompt = f"""
    Identify risks and dependencies in this user story.

    Include:
    - API dependencies
    - Cross-team dependencies
    - Edge cases
    - Data risks

    Output in bullet points.

    Story:
    {story}
    """
    return call_llm(prompt)


# 🔹 4. Test Case Generator
#def generate_test_cases(story):
    prompt = f"""
    Generate test cases for the following user story.

    Include:
    - Positive cases
    - Negative cases
    - Edge cases

    Format clearly.

    Story:
    {story}
    """
    return call_llm(prompt)


# 🔹 5. Estimation Engine
#def estimate_story(story):
    prompt = f"""
    Estimate story points for this user story.

    Include:
    - Story Points (1,2,3,5,8,13)
    - Reasoning
    - Complexity factors

    Story:
    {story}
    """
    return call_llm(prompt)


# 🔹 MAIN EXECUTION FLOW
# def main():
def main():
    print("\n🚀 User Story Generator (Fast Mode)\n")
    
    meeting_notes = input("📥 Enter meeting notes:\n\n")

    print("\n⏳ Generating user story...\n")

    story = generate_user_story(meeting_notes)

    print("\n" + "="*60)
    print("🧾 USER STORY")
    print("="*60)
    print(story)

    # ✅ SAVE OUTPUT HERE
    with open("outputs.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write("INPUT:\n" + meeting_notes + "\n\n")
        f.write("OUTPUT:\n" + story + "\n")
    

if __name__ == "__main__":
    main()

    