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
    import re

    if not story_text or "Title:" not in story_text or "Acceptance Criteria:" not in story_text:
        raise ValueError(f"Invalid story — missing required sections: {str(story_text)[:100]}")

    # ---------- Extract Title ----------
    title_match = re.search(r"Title:\s*(.+)", story_text)
    title = title_match.group(1).strip() if title_match else "User Story"

    title = re.sub(r"\*\*|User Story \d+:\s*", "", title).strip()

    # ---------- Extract Description ----------
    desc_match = re.search(r"Description:\s*(.*?)(Acceptance Criteria:)", story_text, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # ---------- Extract AC ----------
    ac_match = re.search(r"Acceptance Criteria:\s*(.*)", story_text, re.DOTALL)
    ac_text = ac_match.group(1).strip() if ac_match else ""

    ac_lines = []
    for line in ac_text.split("\n"):
        line = line.strip()
        if line:
            ac_lines.append(line)

    # ---------- BUILD ADF FORMAT ----------
    def text_block(text):
        return {
            "type": "paragraph",
            "content": [{"type": "text", "text": text}]
        }

    adf_description = {
        "type": "doc",
        "version": 1,
        "content": []
    }

    # Add description
    if description:
        adf_description["content"].append(text_block(description))

    # Add AC header
    if ac_lines:
        adf_description["content"].append(text_block("Acceptance Criteria:"))

        for ac in ac_lines:
            adf_description["content"].append(text_block(f"• {ac}"))

    return {
        "fields": {
            "project": {"key": "SCRUM"},
            "summary": title,
            "description": adf_description,  # ✅ FIXED HERE
            "issuetype": {"name": "Story"}
        }
    }