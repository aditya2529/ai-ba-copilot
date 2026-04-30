# jira_client.py

import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://aditya2529.atlassian.net"

EMAIL = st.secrets["JIRA_EMAIL"]
API_TOKEN = st.secrets["JIRA_API_TOKEN"]

def create_jira_issue(payload):
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