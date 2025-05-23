from dotenv import load_dotenv
import requests, os

load_dotenv()
def aban_response_taker(full_path) :
    headers = {
        'Authorization': os.getenv('API_KEY_ABAN')
    }
    
    response = requests.get(f'https://abantether.com{full_path}', headers=headers)
    
    return response