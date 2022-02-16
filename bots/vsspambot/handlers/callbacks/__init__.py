from aiogram import Dispatcher

from bots.vsspambot.data.config import ADMIN_COMMANDS, EDIT_COMMANDS, CREATOR_COMMANDS
from bots.vsspambot.data.config import flags
from bots.vsspambot.keyboards.inline.guardian_keyboard import not_bot_callback
from bots.vsspambot.keyboards.inline.settings_keyboard import lang_callback, sets_callback
from .inline import (button_admin_handler, button_edit_handler, button_language_handler, button_not_bot_handler,
                     button_params_buttons)

admin_commands = [ac.replace('/', '') for ac in ADMIN_COMMANDS.keys()]
creator_commands = [ac.replace('/', '') for ac in CREATOR_COMMANDS.keys()]
edited_commands = [ac.replace('/', '') for ac in EDIT_COMMANDS.keys()]
lang_list = [f'lang:{lang}' for lang in flags.keys()]


def register_handlers_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(button_params_buttons, sets_callback.filter(command=('settings')))
    dp.register_callback_query_handler(button_admin_handler, sets_callback.filter(command=creator_commands))
    dp.register_callback_query_handler(button_admin_handler, sets_callback.filter(command=admin_commands))
    dp.register_callback_query_handler(button_edit_handler, sets_callback.filter(command=edited_commands))
    dp.register_callback_query_handler(button_language_handler, lang_callback.filter())
    dp.register_callback_query_handler(button_not_bot_handler, not_bot_callback.filter())
