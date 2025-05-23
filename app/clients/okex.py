from dotenv import load_dotenv
import requests, json, os, datetime, hmac, hashlib, base64

load_dotenv()
def okex_response_taker(full_path, request_method, request_data=None):
    timestamp = int(datetime.datetime.utcnow().now().timestamp() * 1000)
    msg = f'{request_method.upper()}\n{full_path}\n{timestamp}'

    if request_data:
        base64encode = base64.b64encode(json.dumps(request_data).encode()).decode()
        msg += f'\n{base64encode}'

    signed_key = hmac.new(
        bytes(os.getenv('SECRET_KEY_OKEX'), "utf-8"),
        msg=bytes(msg, "utf-8"),
        digestmod=hashlib.sha256).hexdigest()

    headers = {
    'Content-Type': 'application/json',
    'x-api-key': os.getenv('API_KEY_OKEX'),
    'x-signature': signed_key,
    'x-timestamp': f'{timestamp}'
    }
    
    response = requests.get(f'https://azapi.ok-ex.io{full_path}', headers=headers)
    response = json.loads(response.text)
    
    return response