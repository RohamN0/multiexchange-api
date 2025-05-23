from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..clients.okex import okex_response_taker
from ..clients.aban import aban_response_taker
from typing import Annotated


router = APIRouter(prefix="/api")
security = HTTPBasic()

@router.get('/balance')
async def balance(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) :
    aban_balance_response = aban_response_taker('/api/v1/users/balance/')
    usdt_to_irt_response = aban_response_taker('/api/v1/otc/coin-price?coin=USDT')
    okex_balance_response = okex_response_taker('/oapi/v1/wallet', 'GET')
    
    usdt_price = float(usdt_to_irt_response['USDT']['irtPriceBuy'])

    i = 0
    for coin in aban_balance_response :
        coin_response = aban_response_taker(f'/api/v1/otc/coin-price?coin={coin['symbol']}')

        aban_balance = float(coin['balance'])
        aban_coin_price = float(coin_response[f'{coin['symbol']}']['usdtPrice'])
        
        aban_balance_response[i]['irt_price'] = aban_balance * aban_coin_price * usdt_price if coin['symbol'] != 'IRT' else aban_balance
        aban_balance_response[i]['usdt_price'] = aban_balance * aban_coin_price if coin['symbol'] != 'IRT' else aban_balance / usdt_price
        
        i += 1
    
    response = { f'{coin['symbol']}': { 'balance': float(coin['balance']), 'irt_price': coin['irt_price'], 'usdt_price': coin['usdt_price'] } for coin in aban_balance_response }
    
    coins = [coin for coin in response] 

    for coin in okex_balance_response['wallets'] :
        okex_coin_price = okex_response_taker(f'/oapi/v1/otc/ticker?asset={coin['asset']}', 'GET')

        okex_balance = float(coin['otc_balance'])
        okex_coin_price = float(okex_coin_price['ticker'][0]['buy_px']) / usdt_price if coin['asset'] != 'IRT' else 1
        
        if coin['asset'] in coins :
            response[coin['asset']]['balance'] += okex_balance
            response[coin['asset']]['usdt_price'] += okex_balance * okex_coin_price if coin['asset'] != 'IRT' else okex_balance / usdt_price
            response[coin['asset']]['irt_price'] += okex_balance * okex_coin_price * usdt_price if coin['asset'] != 'IRT' else okex_balance
        else :
            response.update({ 
                coin['asset'] : { 
                    'balance' : okex_balance, 
                    'usdt_price' : okex_balance * okex_coin_price if coin['asset'] != 'IRT' else okex_balance / usdt_price,
                    'irt_price' : okex_balance * okex_coin_price * usdt_price if coin['asset'] != 'IRT' else okex_balance
                }
            })
            
    okex_withdraw = okex_response_taker('/oapi/v1/wallet/withdrawal/history', 'GET')
                
    for coin in okex_withdraw['data'] :
        okex_coin_price = okex_response_taker(f'/oapi/v1/otc/ticker?asset={coin['asset']}', 'GET')
        
        okex_balance = coin['amount']
        okex_coin_price = float(okex_coin_price['ticker'][0]['buy_px']) / usdt_price if coin['asset'] != 'IRT' else 1
        
        if coin['asset'] in coins :
            response[coin['asset']]['balance'] += okex_balance
            response[coin['asset']]['usdt_price'] += okex_balance * okex_coin_price if coin['asset'] != 'IRT' else okex_balance / usdt_price
            response[coin['asset']]['irt_price'] += okex_balance * okex_coin_price * usdt_price if coin['asset'] != 'IRT' else okex_balance
        else :
            response.update({ 
                coin['asset'] : { 
                    'balance' : okex_balance, 
                    'usdt_price' : okex_balance * okex_coin_price if coin['asset'] != 'IRT' else okex_balance / usdt_price,
                    'irt_price' : okex_balance * okex_coin_price * usdt_price if coin['asset'] != 'IRT' else okex_balance
                }
            })
    
    return response