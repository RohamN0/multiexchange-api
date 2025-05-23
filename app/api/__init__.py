from .balance import router as balance_router
from .buy_average import router as buy_average_router
from .sell_average import router as sell_average_router
from .news import router as news_router
from .eco_calendar import router as eco_calendar_router
from .coins import router as coins_router

__all__ = [
    "balance_router", "buy_average_router", "sell_average_router",
    "news_router", "eco_calendar_router", "coins_router"
]