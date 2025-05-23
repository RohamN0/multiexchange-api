from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests
from bs4 import BeautifulSoup

router = APIRouter(prefix="/api")
security = HTTPBasic()

@router.get('/news')
async def news(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
    response = requests.get(url)
    
    bs = BeautifulSoup(response.content, 'html.parser')
    tags = bs.find_all('article', class_='IBr9hb')
    
    data = { f'{i}': { 'text': tags[i].find_all('a')[1].text, 
                      'url': 'https://news.google.com' + str(tags[i].find_all('a')[1]).split('href=".')[1].split('"')[0] 
                    } for i in range(len(tags)) }
    
    return data