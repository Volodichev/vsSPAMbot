import asyncio
import logging

from bots.vsspambot.loader import dp, on_startup

async def run_polling():
    from bots.vsspambot import middlewares, filters, handlers
    await on_startup()
    await dp.start_polling(reset_webhook=True)
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    asyncio.run(run_polling())
