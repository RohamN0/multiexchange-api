from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..clients.okex import okex_response_taker

router = APIRouter(prefix="/api")
security = HTTPBasic()

@router.get('/coins')
async def coins(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return okex_response_taker('/oapi/v1/otc/tickers', 'GET')