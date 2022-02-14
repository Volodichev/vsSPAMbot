from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bots.vsspambot.utils import isolate_commands


class ConfMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # await print_handler(message, sys._getframe().f_code.co_name)

        text = message.text
        if text:
            word_list = text.split()
            if len(word_list) > 1:
                custom_commands = await isolate_commands(message)
                data["custom_commands"] = custom_commands

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        # await print_handler(query, sys._getframe().f_code.co_name)
        pass
