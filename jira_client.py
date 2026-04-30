import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://aditya2529.atlassian.net"

def create_jira_issue(payload):
    EMAIL = st.secrets.get("JIRA_EMAIL")
    API_TOKEN = st.secrets.get("JIRA_API_TOKEN")

    if not EMAIL or not API_TOKEN:
        raise Exception("JIRA secrets not loaded. Check Streamlit Cloud secrets.")

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