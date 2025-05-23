from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests

router = APIRouter(prefix="/api")
security = HTTPBasic()

@router.get('/eco-cal')
async def economic_calendar(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'
    response = requests.get(url)
    response = response.json()
    
    return response