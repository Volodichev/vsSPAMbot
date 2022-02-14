from aiogram.types import ChatType, Message

chat_types = [ChatType.PRIVATE]

async def command_start_handler(message: Message):
    bot_name = 'vsspambot'
    text = \
        f' Hey, I am {bot_name} Bot!\n' \
        f' \n' \
        f' I kill spam. I remove links and forwarded messages by users joined chat less than N hours ago\n' \
        f' \n' \
        f' - Documentation and FAQ: vsspambot (https://github.com/volodichev/vsspambot)'

    await message.answer(text)

async def command_help_handler(message: Message):
    bot_name = 'vsspambot'
    text = \
        f' Hey, I am {bot_name} Bot!\n' \
        f' \n' \
        f' I kill spam. I remove links and forwarded messages by users joined chat less than N hours ago\n' \
        f' \n' \
        f' - Documentation and FAQ: vsspambot (https://github.com/volodichev/vsspambot)'

    await message.answer(text)

