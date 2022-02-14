from bots.vsspambot.loader import dp
import logging

from .commands import ConfMiddleware
from .throttling import ThrottlingMiddleware

if __name__ == "bots.vsspambot.middlewares":
    dp.middleware.setup(ConfMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    logging.info(f"Middlewares are successfully configured")
