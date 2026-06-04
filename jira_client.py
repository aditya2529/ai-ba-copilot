import os
import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://aditya2529.atlassian.net"


def _get_jira_credentials():
    """Resolve Jira credentials.

    Tries Streamlit secrets first (for the web app), then falls back to
    environment variables (for the MCP server / headless usage). This lets
    the same function work both inside Streamlit and outside it.
    """
    email = None
    token = None

    # Streamlit secrets (only available when running under Streamlit)
    try:
        import streamlit as st
        email = st.secrets.get("JIRA_EMAIL")
        token = st.secrets.get("JIRA_API_TOKEN")
    except Exception:
        pass

    # Environment-variable fallback
    if not email:
        email = os.getenv("JIRA_EMAIL")
    if not token:
        token = os.getenv("JIRA_API_TOKEN")

    return email, token


def create_jira_issue(payload):
    EMAIL, API_TOKEN = _get_jira_credentials()

    if not EMAIL or not API_TOKEN:
        raise Exception(
            "JIRA credentials not found. Set them in Streamlit secrets "
            "(JIRA_EMAIL / JIRA_API_TOKEN) or as environment variables."
        )

    url = f"{JIRA_URL}/rest/api/3/issue"

    response = requests.post(
        url,
        json=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    return response
