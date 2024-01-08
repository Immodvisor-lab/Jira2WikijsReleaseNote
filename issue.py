from jira.get_image import get_image
from wiki_js.upload_image import upload_image
import re
from dotenv import load_dotenv
import os
from jira2markdown import convert

load_dotenv()

class Issue:
    def __init__(self, jira_issue):
        self.key = jira_issue[os.getenv("JIRA_FIELD_KEY")]
        print('-- processing issue '+self.key+'...')
        #print(json.dumps(jira_issue, indent=4))
        self.title = jira_issue['fields'][os.getenv("JIRA_FIELD_TITLE")]
        self.content = jira_issue['fields'][os.getenv("JIRA_FIELD_CONTENT")]
        self.link = os.getenv("JIRA_URL") + "/browse/" + self.key
        attachments = jira_issue['fields'][os.getenv("JIRA_FIELD_ATTACHMENT")]
        self.attachments = attachments if attachments is not None else []
        self.image_path = "/releases-notes/"

    def upload_attachments(self):
        if len(self.attachments) == 0:
            return "Nothing attached to "+self.key
        
        for attachment in self.attachments:
            if attachment['filename'] in self.content:
                if attachment['content'] and attachment['mimeType'] == 'image/png':
                    image = get_image(attachment['content'])
                    response = upload_image(attachment['filename'], image, self.image_path)
                    print(response)
                else:
                    print("Attachment found but it's not a .png : "+attachment['filename']+" for the issue "+self.key)

    def update_img_src(self,html_string):
        # Define the regex pattern to match <img> tags and extract src attribute
        img_pattern = re.compile(r'<img\s+([^>]*)src\s*=\s*["\'](.*?)["\']([^>]*)>', re.IGNORECASE)

        def update_src(match):
            img_attributes_before = match.group(1)
            src = match.group(2)
            img_attributes_after = match.group(3)

            updated_src = f'src="{self.image_path}{src}"'
            updated_img_tag = f'<img {img_attributes_before}{updated_src}{img_attributes_after}>'

            return updated_img_tag

        # Use re.sub to replace matched occurrences in the HTML string
        updated_html = img_pattern.sub(update_src, html_string)

        return updated_html

    def format_content(self):
        if isinstance(self.content, str): 
            self.content = convert(self.content)
            self.content = self.update_img_src(self.content)
        else: 
            self.content = 'There is no content for this issue'
            return False


    def get_final_content(self):
        return f'# {self.key} - {self.title} \n [Lien vers Jira]({self.link}) \n\n {self.content} \n'