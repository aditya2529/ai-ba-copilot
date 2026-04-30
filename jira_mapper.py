def format_description(story_text):
    lines = story_text.split("\n")

    content = []

    def add_heading(text):
        content.append({
            "type": "heading",
            "attrs": {"level": 3},
            "content": [{"type": "text", "text": text}]
        })

    def add_paragraph(text):
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": text}]
        })

    def add_bullets(items):
        content.append({
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": item}]
                    }]
                } for item in items
            ]
        })

    # -------- PARSING --------
    user_story = []
    description = []
    acceptance = []
    assumptions = []
    notes = []
    examples = []

    current = "desc"  # default

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Section detection
        if "Acceptance Criteria" in line:
            current = "ac"
            continue
        elif "Assumptions" in line:
            current = "assumptions"
            continue
        elif "Notes" in line:
            current = "notes"
            continue
        elif "Example" in line:
            current = "example"
            continue

        clean_line = line.replace("*", "").strip("- ").strip()
        if clean_line.lower().startswith("title"):
            continue

        # Capture user story line
        if clean_line.lower().startswith("as a"):
            user_story.append(clean_line)
            continue

        if current == "desc":
            description.append(clean_line)
        elif current == "ac":
            acceptance.append(clean_line)
        elif current == "assumptions":
            assumptions.append(clean_line)
        elif current == "notes":
            notes.append(clean_line)
        elif current == "example":
            examples.append(clean_line)

    # -------- BUILD ADF --------

    if user_story:
        add_heading("User Story")
        for us in user_story:
            add_paragraph(us)

    if description:
        add_heading("Description")
        for d in description:
            add_paragraph(d)

    if acceptance:
        add_heading("Acceptance Criteria")
        add_bullets(acceptance)

    if examples:
        add_heading("Examples")
        add_bullets(examples)

    if assumptions:
        add_heading("Assumptions")
        add_bullets(assumptions)

    if notes:
        add_heading("Notes")
        add_bullets(notes)

    return {
        "type": "doc",
        "version": 1,
        "content": content
    }


def map_to_jira_payload(story_text):

    clean_summary = ""

    for line in story_text.split("\n"):
        line = line.strip().replace("*", "")

        if line.lower().startswith("title"):
            clean_summary = line.split(":", 1)[1].strip()
            break

    # fallback if Title not found
    if not clean_summary:
        for line in story_text.split("\n"):
            if line.lower().startswith("as a"):
                clean_summary = line.strip()
                break

    # final fallback
    if not clean_summary:
        clean_summary = story_text.replace("\n", " ")[:100]

    return {
        "fields": {
            "project": {"key": "SCRUM"},
            "summary": clean_summary[:100],
            "description": format_description(story_text),
            "issuetype": {"name": "Story"}
        }
    }