import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

def search_issues_in_version(version):

    jql = f'project = {os.getenv("JIRA_PROJECT")} AND issuetype = "{os.getenv("JIRA_ISSUE_TYPE")}" AND fixVersion = "{version}"'

    if os.getenv("EXTRA_JQL"):
       jql += os.getenv("EXTRA_JQL")

    api_endpoint_search = f'{os.getenv("JIRA_URL")}/rest/api/2/search'
    params = {
        'jql': jql,
        'fields': [
            os.getenv("JIRA_FIELD_KEY"),
            os.getenv("JIRA_FIELD_TITLE"),
            os.getenv("JIRA_FIELD_CONTENT"),
            os.getenv("JIRA_FIELD_ATTACHMENT"),
        ]
    }

    jira_answer = requests.post(
        api_endpoint_search, 
        auth=HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_PASSWORD")),
        json=params
    )

    if jira_answer.status_code != 200:
        print("Call to Jira returned with code "+str(jira_answer.status_code))
        raise Exception("Failed to search for issues. Check if your version does not have remaining spaces. Error: "+str(jira_answer.content))

    issues = jira_answer.json()['issues']

    if len(issues) == 0:
        raise Exception("This version contains no "+os.getenv("JIRA_ISSUE_TYPE"))

    return issues