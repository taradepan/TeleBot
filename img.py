import requests
import os
from PIL import Image, UnidentifiedImageError
import io
import dotenv
dotenv.load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer "+os.environ.get('HF_TOKEN')}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  
    return response.content

def img(prompt):
    result = query({
        "inputs": prompt,
    })
    try:
        Image.open(io.BytesIO(result))  
    except UnidentifiedImageError:
        raise ValueError("The API response is not a valid image")
    return result