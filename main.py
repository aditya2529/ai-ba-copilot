from story_generator import generate_user_story
from validator import validate_story
from logger import log

log("Generating user story")
log("Validation triggered")

def main():
    notes = input("Enter meeting notes:\n")

    story = generate_user_story(notes)
    print("\nUSER STORY:\n", story)

    choice = input("\nDo you want to validate this story? (y/n): ")

    if choice.lower() == 'y':
        validation = validate_story(story)
        print("\nVALIDATION:\n", validation)

if __name__ == "__main__":
    main()