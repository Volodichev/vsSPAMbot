import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode

from apps.db.models.base import BaseModel
from bots.vsspambot.db.models import VsSpamBotUserDB, VsSpamBotSettings
from bots.vsspambot.data.config import BOT_TOKEN, REDIS_PARAMS

# Configure logging
# os.chdir('/home/restapi')
logging.basicConfig(
    level=logging.getLevelName("INFO"),  # "DEBUG" "INFO"
    format="%(asctime)s [%(levelname)7s]:  %(message)40s   ||  %(name)s  ||  (%(filename)s).%(funcName)s(%(lineno)d) ",
    datefmt='%d/%m|%H:%M:%S',
    handlers=[
        logging.FileHandler(f'{os.path.basename(__file__)}.log'),
        logging.StreamHandler(sys.stdout), ])

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)


storage = RedisStorage2(**REDIS_PARAMS) if REDIS_PARAMS else MemoryStorage()

dp = Dispatcher(bot, storage=storage)
db = {'base': BaseModel(), 'botusers': VsSpamBotUserDB(), 'botsets': VsSpamBotSettings()}


async def on_startup():
    from bots.vsspambot.utils.bases import init_bases_params

    # todo: раскомментить позже
    # await setup_default_commands(dp)
    await init_bases_params()


async def on_shutdown():
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


__all__ = (
    "on_startup",
    "bot",
    "storage",
    "dp",
    "db"
)
