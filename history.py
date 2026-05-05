import json
import os
import re
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")
MAX_ENTRIES = 50


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_history(mode, meeting_notes, story, validation=None, risks=None, test_cases=None, estimation=None):
    titles = re.findall(r"Title:\s*(.+)", story or "")
    entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
        "mode": mode,
        "input_preview": (meeting_notes[:70].strip() + "...") if len(meeting_notes) > 70 else meeting_notes.strip(),
        "story_titles": titles[:2],
        "meeting_notes": meeting_notes,
        "story": story,
        "validation": validation,
        "risks": risks,
        "test_cases": test_cases,
        "estimation": estimation,
    }
    history = load_history()
    history.insert(0, entry)
    history = history[:MAX_ENTRIES]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    return entry
