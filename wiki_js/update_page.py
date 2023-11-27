import requests
from dotenv import load_dotenv
import os

load_dotenv()

def update_page(id, content, description, tags, title):

    # GraphQL mutation to create a page
    mutation = f'''
        mutation Page {{
            pages {{
                update (id:{id} ,content:"""{content}""", description:"{description}", editor: "markdown", isPublished: true, isPrivate: false, locale: "fr", tags: ["{tags}"], title:"{title}") {{
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