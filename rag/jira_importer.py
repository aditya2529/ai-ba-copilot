"""Pull past Story-type issues from Jira via REST API and normalise into corpus text.

Reuses the same Atlassian basic-auth pattern as `jira_client.py` (Streamlit
secrets first, env-var fallback). Paginates through all stories in project SCRUM.
"""

import os
from typing import List, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://aditya2529.atlassian.net"
PROJECT_KEY = "SCRUM"  # matches jira_mapper.py
PAGE_SIZE = 50


def _get_auth():
    """Try Streamlit secrets first, then environment variables."""
    email = None
    token = None
    try:
        import streamlit as st
        email = st.secrets.get("JIRA_EMAIL")
        token = st.secrets.get("JIRA_API_TOKEN")
    except Exception:
        pass
    if not email:
        email = os.getenv("JIRA_EMAIL")
    if not token:
        token = os.getenv("JIRA_API_TOKEN")
    if not email or not token:
        raise RuntimeError("JIRA_EMAIL / JIRA_API_TOKEN not configured (secrets or env).")
    return HTTPBasicAuth(email, token)


def _adf_to_text(node) -> str:
    """Flatten an Atlassian Document Format node tree into plain text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "\n".join(_adf_to_text(n) for n in node if n)
    if isinstance(node, dict):
        node_type = node.get("type")
        # Leaf text node
        if node_type == "text":
            return node.get("text", "")
        # Recurse into children
        children = node.get("content") or []
        text = _adf_to_text(children)
        # Add separators for block elements
        if node_type in ("paragraph", "heading", "listItem", "bulletList", "orderedList"):
            return text + "\n"
        return text
    return ""


def fetch_stories(max_results: Optional[int] = None) -> List[Dict]:
    """Fetch all Story-type issues from the configured Jira project.

    Returns a list of dicts: {key, summary, description, normalised_text}.
    `normalised_text` is the format we feed to the vector store.
    """
    auth = _get_auth()
    headers = {"Accept": "application/json"}

    issues_out: List[Dict] = []
    next_page_token: Optional[str] = None

    # New endpoint: /rest/api/3/search/jql (the old /search was removed by
    # Atlassian — see https://developer.atlassian.com/changelog/#CHANGE-20).
    # Pagination is now via nextPageToken instead of startAt; there is no
    # "total" field — loop until isLast=True or nextPageToken is missing.
    while True:
        params = {
            "jql": f'project = {PROJECT_KEY} AND issuetype = Story',
            "maxResults": PAGE_SIZE,
            "fields": "summary,description",
        }
        if next_page_token:
            params["nextPageToken"] = next_page_token

        url = f"{JIRA_URL}/rest/api/3/search/jql"
        resp = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Jira fetch failed: {resp.status_code} {resp.text[:200]}")
        data = resp.json()
        issues = data.get("issues", []) or []
        if not issues:
            break

        for issue in issues:
            key = issue.get("key")
            fields = issue.get("fields", {}) or {}
            summary = fields.get("summary", "") or ""
            description_adf = fields.get("description")
            description = _adf_to_text(description_adf).strip()
            normalised = _normalise_story(summary, description)
            issues_out.append({
                "key": key,
                "summary": summary,
                "description": description,
                "normalised_text": normalised,
            })

        if max_results and len(issues_out) >= max_results:
            issues_out = issues_out[:max_results]
            break

        # Continue if more pages exist
        next_page_token = data.get("nextPageToken")
        is_last = data.get("isLast", True)
        if is_last or not next_page_token:
            break

    return issues_out


def _normalise_story(summary: str, description: str) -> str:
    """Format a Jira issue into our canonical Title/Description/AC layout (best-effort).

    If the description already contains "Acceptance Criteria" we preserve it
    as-is; otherwise we wrap everything under Description.
    """
    summary = (summary or "").strip()
    description = (description or "").strip()

    parts = [f"Title: {summary}"] if summary else []
    if "Acceptance Criteria" in description:
        # description already contains AC — split and re-stitch
        idx = description.find("Acceptance Criteria")
        desc_body = description[:idx].strip()
        ac_body = description[idx:].strip()
        if desc_body:
            parts.append(f"Description:\n{desc_body}")
        parts.append(ac_body)
    else:
        if description:
            parts.append(f"Description:\n{description}")

    return "\n\n".join(parts)
