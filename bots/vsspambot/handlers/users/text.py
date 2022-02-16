import sys
from aiogram.types import Message
from bots.vsspambot.utils.manage import print_handler


async def command_handler(message: Message):
    await print_handler(message, sys._getframe().f_code.co_name)
    """
    Handler for unknown command.
    """
    # await print_handler(message, sys._getframe().f_code.co_name)
    return

async def text_handler(message: Message):
    await print_handler(message, sys._getframe().f_code.co_name)
    """
    Handler for unknown messages.
    """
    # await print_handler(message, sys._getframe().f_code.co_name)
    return
