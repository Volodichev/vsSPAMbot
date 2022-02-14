from bots.vsspambot.utils.manage import get_commands
from bots.vsspambot.data.config import ADMIN_COMMANDS, CREATOR_COMMANDS, EDIT_COMMANDS
from aiogram.dispatcher.handler import CancelHandler
from bots.vsspambot.data.localizations import commands_descriptions, commands_emoji

from bots.vsspambot.handlers.groups.admins import command_quarantine_handler, command_admin_handler, command_creator_handler, show_language_buttons
from bots.vsspambot.handlers.groups.text import command_handler


from aiogram.types import BotCommand
import logging

# log = logging.getLogger('default_commands')

async def is_command(message) -> bool:
    """
    Check message text contains commands

    :return: bool
    """
    return any([ent.type == "bot_command" for ent in message.entities])


async def isolate_commands(message):
    """
    Get commands from message

    """
    if not await is_command(message):
        logging.debug(f'в сообщении нет комманд')
        return

    cancelhandler = False
    commands = await get_commands(message)
    command_keys = commands.keys()
    message_text = message.text

    if message.chat.type != 'private':
        if len(command_keys) > 0:
            cancelhandler = True

            for command, parametr in commands.items():

                if parametr:
                    text_command = f'{command} {parametr}'
                else:
                    text_command = command
                message.text = f'{text_command}'

                if command in CREATOR_COMMANDS.keys():
                    await command_creator_handler(message)
                elif command in ADMIN_COMMANDS.keys():
                    await command_admin_handler(message)
                elif command in EDIT_COMMANDS.keys():

                    if command == '/quarantine':
                        await command_quarantine_handler(message)
                    elif command == '/language':
                        await show_language_buttons(message)

                else:
                    await command_handler(message)

            if not message_text.startswith('/'):
                cancelhandler = False

        message.text = message_text

    if cancelhandler:
        raise CancelHandler()

    return commands

async def setup_default_commands(dp):
    bot = dp.bot
    await bot.delete_my_commands()
    for language_code, command_list in commands_descriptions.items():
        commands = list()
        if command_list is None:
            command_list = commands_descriptions.get('en')

        for command, desc in command_list.items():
            emoji = commands_emoji.get(command)
            description = f"{emoji}{desc}"
            commands.append(BotCommand(command=command, description=description))


        await bot.set_my_commands(commands=commands, language_code=language_code)
        print(f'commandes:{language_code=} ok')
    logging.info(f'Standard commands are successfully configured')


