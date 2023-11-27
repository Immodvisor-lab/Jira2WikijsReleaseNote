import requests
from dotenv import load_dotenv
import os

load_dotenv()

def create_page(content, description, path, tags, title):

    # GraphQL mutation to create a page
    mutation = f'''
        mutation Page {{
            pages {{
                create (content:"""{content}""", description:"{description}", editor: "markdown", isPublished: true, isPrivate: false, locale: "fr", path:"{path}", tags: ["{tags}"], title:"{title}") {{
                responseResult {{
                    succeeded,
                    errorCode,
                    slug,
                    message
                }},
                page {{
                    id,
                    path,
                    title
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

    if response.status_code != 200:
        raise Exception(response.content)