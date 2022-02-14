from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bots.vsspambot.data.config import langs, flags
from bots.vsspambot.utils.bases import get_params_commands

lang_callback = CallbackData('languge', 'chat_id', 'lang')  # languge:<chat_id>:<language_code>


async def generate_language_markup(chat_id: int, lang='en') -> InlineKeyboardMarkup:
    """
    Generate keyboard
    """
    lang_keyboard_markup = InlineKeyboardMarkup(row_width=3)
    for language, lang_code in langs.items():
        flag = flags.get(lang_code)

        text = f'{flag} {language}'
        if lang_code == lang:
            text = f'>>{text}<<'

        lang_keyboard_markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=lang_callback.new(
                    chat_id=chat_id,
                    lang=lang_code,
                )
            )
        )

    return lang_keyboard_markup


async def generate_settings_markup(chat_id: int, lang='en') -> InlineKeyboardMarkup:
    param_dict = await get_params_commands(chat_id=chat_id)
    keyboard_markup = InlineKeyboardMarkup(row_width=2)

    for p, command in param_dict.items():
        keyboard_markup.insert(
            InlineKeyboardButton(text=p, callback_data=command),
        )

    return keyboard_markup
