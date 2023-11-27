import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def search_page(query):

    # GraphQL mutation to create a page
    mutation = f'''
        query {{
            pages {{
                search (query:"""{query}"""){{
                    results{{
                        id
                        title
                        path
                        locale
                    }}
                }}
            }}
        }}
    '''

    response = requests.request(
        "POST", 
        os.getenv("WIKIJS_BASE_URL")+"/graphql",
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+os.getenv("WIKIJS_BEARER_TOKEN")
        },
        json={'query': mutation})

    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data['data']['pages']['search']['results'][0]['id']
    else:
        return 'Failed to search wiki page. Got '+response.status_code