import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

def get_versions():

    api_endpoint_versions = f'{os.getenv("JIRA_URL")}/rest/api/latest/project/{os.getenv("JIRA_PROJECT")}/versions'

    jira_answer = requests.get(api_endpoint_versions, auth=HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_PASSWORD")))

    if jira_answer.status_code != 200:
        print("Call to Jira returned with code "+str(jira_answer.status_code))
        raise Exception("Failed to search for versions.")

    versions = jira_answer.json()

    # Filter versions with "released" set to true and not archived

    unreleased_versions = [version for version in versions if (not version.get('released') and not version.get('archived'))]
    
    # Extract and format the desired information
    unreleased_version_info = [
        {
            'id': version['id'],
            'name': version['name'],
            'releaseDate': version['releaseDate']
        }
        for version in unreleased_versions
    ]

    return unreleased_version_info