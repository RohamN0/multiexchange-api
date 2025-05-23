from fastapi import FastAPI
from .api.balance import router as balance_router
from .api.buy_average import router as buy_router
from .api.sell_average import router as sell_router
from .api.news import router as news_router
from .api.eco_calendar import router as eco_router
from .api.coins import router as coins_router

app = FastAPI()

app.include_router(balance_router)
app.include_router(buy_router)
app.include_router(sell_router)
app.include_router(news_router)
app.include_router(eco_router)
app.include_router(coins_router)