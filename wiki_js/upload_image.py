import requests
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()

def check_image_exists(dir_path, filename):
    base_url = os.getenv("WIKIJS_BASE_URL")
    image_url = f"{base_url}{dir_path}{filename}"
    response = requests.get(
        image_url,
        headers={
            'Authorization': 'Bearer '+os.getenv("WIKIJS_BEARER_TOKEN")
        }, 
    )
    return response.status_code == 200

def upload_image(filename, image, dir_path):

    if check_image_exists(dir_path,filename):
        return "Image "+filename+" already exists."

    openImage = Image.open(io.BytesIO(image.content))

    def convert_pil_image_to_byte_array(img):
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG', subsampling=0, quality=100)
        img_byte_array = img_byte_array.getvalue()
        return img_byte_array

    converted_image = convert_pil_image_to_byte_array(openImage)

    files = (
        ('mediaUpload', (None, '{"folderId":'+os.getenv("WIKIJS_UPLOADED_IMAGES_FOLDER_ID")+'}')), 
        ('mediaUpload', (filename, converted_image, 'image/png'))
    )

    result = requests.post(
        os.getenv("WIKIJS_BASE_URL")+'/u', 
        headers={
            'Authorization': 'Bearer '+os.getenv("WIKIJS_BEARER_TOKEN")
        }, 
        files=files
    ) 

    return "Image "+filename+" uploaded to WikiJS : "+result.text