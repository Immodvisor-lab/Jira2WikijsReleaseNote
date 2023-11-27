import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

def get_image(url):
    return requests.get(url, auth=HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_PASSWORD")))
