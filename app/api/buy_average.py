from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..clients.okex import okex_response_taker
from ..clients.aban import aban_response_taker

router = APIRouter(prefix="/api")
security = HTTPBasic()

@router.get('/buy_average')
async def buy_avg(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    usdt_to_irt_response = aban_response_taker('/api/v1/otc/coin-price?coin=USDT')
    aban_buy_response = aban_response_taker('/api/v1/otc/orders/buy/?page=1&count=20')
    okex_buy_response = okex_response_taker('/oapi/v1/trade/otc/history?side=buy', 'GET')

    currency = { data['asset'] : { 'amount': [], 'coinPrice_irt': [], 'irtPrice': [], 
            'avrg_amount': 0, 'avrg_coinPrice_irt': 0, 
            'avrg_irtPrice': 0 } for data in okex_buy_response['data'] }
    currency.update({ data['coinSymbol'] : 
        { 'amount': [], 'coinPrice_usdt': [], 'coinPrice_irt': [], 'usdtPrice': [], 
         'irtPrice': [], 'tetherPrice': [], 'avrg_amount': 0, 'avrg_coinPrice_usdt': 0, 
         'avrg_coinPrice_irt': 0, 'avrg_usdtPrice': 0, 'avrg_irtPrice': 0, 
         'avrg_tetherPrice': 0 } for data in aban_buy_response['orders'] })
    
    
    for data in aban_buy_response['orders'] :
        currency[f'{data['coinSymbol']}']['amount'].append(float(data['amount']))
        currency[f'{data['coinSymbol']}']['coinPrice_usdt'].append(float(data['coinPrice']))
        currency[f'{data['coinSymbol']}']['coinPrice_irt'].append(float(data['coinPrice']) * float(usdt_to_irt_response['USDT']['irtPriceBuy']))
        currency[f'{data['coinSymbol']}']['usdtPrice'].append(float(data['usdtPrice']))
        currency[f'{data['coinSymbol']}']['irtPrice'].append(float(data['irtPrice']))
        currency[f'{data['coinSymbol']}']['tetherPrice'].append(float(data['tetherPrice']))   
    
    for data in okex_buy_response['data'] :
        currency[f'{data['asset']}']['amount'].append(float(data['amount']))
        currency[f'{data['asset']}']['coinPrice_irt'].append(float(data['amount_rial']) / float(data['amount']))
        currency[f'{data['asset']}']['irtPrice'].append(float(data['amount_rial']))
    
    for coin in currency :
        if len(currency[f'{coin}']) != 6 :
            currency[f'{coin}']['avrg_amount'] = sum(currency[f'{coin}']['amount']) / len(currency[f'{coin}']['amount'])
            currency[f'{coin}']['avrg_coinPrice_usdt'] = sum(currency[f'{coin}']['coinPrice_usdt']) / len(currency[f'{coin}']['coinPrice_usdt'])
            currency[f'{coin}']['avrg_coinPrice_irt'] = sum(currency[f'{coin}']['coinPrice_irt']) / len(currency[f'{coin}']['coinPrice_irt'])
            currency[f'{coin}']['avrg_usdtPrice'] = sum(currency[f'{coin}']['usdtPrice']) / len(currency[f'{coin}']['usdtPrice'])
            currency[f'{coin}']['avrg_irtPrice'] = sum(currency[f'{coin}']['irtPrice']) / len(currency[f'{coin}']['irtPrice'])
            currency[f'{coin}']['avrg_tetherPrice'] = sum(currency[f'{coin}']['tetherPrice']) / len(currency[f'{coin}']['tetherPrice'])

        else :
            currency[f'{coin}']['avrg_amount'] = sum(currency[f'{coin}']['amount']) / len(currency[f'{coin}']['amount'])
            currency[f'{coin}']['avrg_coinPrice_irt'] = sum(currency[f'{coin}']['coinPrice_irt']) / len(currency[f'{coin}']['coinPrice_irt'])
            currency[f'{coin}']['avrg_irtPrice'] = sum(currency[f'{coin}']['irtPrice']) / len(currency[f'{coin}']['irtPrice'])
        
    return currency