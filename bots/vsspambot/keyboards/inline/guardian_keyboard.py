import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bots.vsspambot.data.localizations import localizations, captcha_emoji

not_bot_callback = CallbackData("confirm_user", "button", "user_id")

async def generate_confirm_markup(user_id: int, lang='en') -> InlineKeyboardMarkup:
    """
    Generate keyboard
    """

    button_list = ['captcha_user_button', 'captcha_bot_button', 'captcha_not_user_button']
    random.shuffle(button_list)

    confirm_no_bot_keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for button in button_list:
        button_name = localizations.get(button).get(lang)
        emoji = captcha_emoji.get(button)
        text = f'{emoji}{button_name}'
        confirm_no_bot_keyboard_markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=not_bot_callback.new(
                    button=button,
                    user_id=user_id,
                )
            )
        )

    return confirm_no_bot_keyboard_markup



