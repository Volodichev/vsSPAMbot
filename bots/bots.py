import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
import aiojobs
from config.settings import BOT_TOKENS
import importlib
import logging

from config.settings import BOT_TOKENS, WEBHOOK_HOST, SSL


async def check_token(name, token):
    return token == BOT_TOKENS.get(name, None)


async def proceed_update(request: web.Request):
    try:
        upds = [types.Update(**(await request.json()))]
    except:
        return

    items = dict(request.query.items())
    name = items.get('name', None)
    if name:
        app_params = request.app.get(name, None)
        if app_params:
            bot = app_params.get('bot', None)
            dp = app_params.get('dp', None)
            if dp:
                Bot.set_current(bot)
                Dispatcher.set_current(dp)
                await dp.process_updates(upds)


async def execute(request: web.Request) -> web.Response:
    items = dict(request.query.items())
    name = items.get('name', '-')
    token = items.get('token', None)
    if await check_token(str(name), str(token)):
        scheduler = request.app['scheduler']
        await scheduler.spawn(proceed_update(request))

    return web.Response(text='ok', status=200)


async def init_webhook_bot(app, BOT_NAME, bot, storage, dp, db):
    BOT_TOKEN = BOT_TOKENS.get(BOT_NAME, None)
    WEBHOOK_PATH = f'/bot?name={BOT_NAME}&token={BOT_TOKEN}'
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    app[BOT_NAME] = {'bot': bot, 'storage': storage, 'dp': dp, 'db': db}

    webhook_status = await bot.delete_webhook()
    print(f'DELETE webhook status: {webhook_status}')

    ssl_data = open(SSL, 'rb')
    certificate = f'@{str(ssl_data)}'
    res = await bot.set_webhook(url=WEBHOOK_URL, certificate=certificate)
    print(f'Configure Webhook URL to: {WEBHOOK_URL} \nwebhook result: {res}')

    webhook_status = await bot.get_webhook_info()
    print(f'webhook status: {webhook_status}')


async def init_webhook_bots(app):
    scheduler = await aiojobs.create_scheduler()
    app['scheduler'] = scheduler

    for BOT_NAME, BOT_TOKEN in BOT_TOKENS.items():
        try:
            loader = importlib.import_module(f'bots.{BOT_NAME}.loader')
            await init_webhook_bot(app, BOT_NAME, loader.bot, loader.storage, loader.dp, loader.db)

            await loader.on_startup()
        except:
            print(f'\n\nНе удалось установить webhook {BOT_NAME} [{BOT_TOKEN}]\n\n')
        await asyncio.sleep(0.3)

    app.router.add_route('*', f'/bot', execute)


async def shutdown_bots(app):
    for BOT_NAME, BOT_TOKEN in BOT_TOKENS.items():
        logging.warning(f"Shutting down {BOT_NAME}..")
        try:
            app_item = app[BOT_NAME]
            dp = app_item.get('dp')
            bot = app_item.get('bot')
            db = app_item.get('db')
            webhook_status = await bot.delete_webhook()
            print(f'DELETE webhook status: {webhook_status}')

            # await dp.bot.session.close()
            # await redis_storage.close()
            await db.close_pool()

            await dp.storage.close()
            await dp.storage.wait_closed()
        except:
            print(f'\n\nНе удалось on_shutdown webhook {BOT_NAME} [{BOT_TOKEN}]\n\n')

# async def shutdown():
#     from bots.vsspambot.loader import on_shutdown
#     await on_shutdown()
