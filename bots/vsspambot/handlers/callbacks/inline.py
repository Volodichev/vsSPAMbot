import asyncio
import sys
from datetime import timedelta as td

from aiogram import types

from bots.vsspambot.data.config import ADMIN_COMMANDS
from bots.vsspambot.keyboards.inline.settings_keyboard import generate_language_markup, generate_settings_markup
from bots.vsspambot.loader import dp
from bots.vsspambot.utils.bases import get_redis_params, put_redis_and_db_params
from bots.vsspambot.utils.manage import (is_bot_admin, send_message, print_handler, edit_message_reply_markup,
                                         edit_message_text, delete_message, kick_chat_member, restrict_chat_member,
                                         get_lang_text)

_ = get_lang_text


async def button_admin_handler(query: types.InlineQuery):
    # await print_handler(query, sys._getframe().f_code.co_name)

    if not 'message' in query:
        return

    no_moderators = None

    bot = dp.bot
    message = query.message
    message_id = message.message_id
    data = query.data
    text = f'/{data}'

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    user_id = query.from_user.id
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    is_chat_creator = user.is_chat_creator()

    if is_chat_creator or is_chat_admin:
        params = await get_redis_params(chat_id)
        no_moderators = params.get('NO_MODERATORS')

    if no_moderators and not is_chat_creator:
        er_text = await _('er_not_creator', lang=lang)
        result_text = f'"{text}":\n{er_text}'
        await send_message(chat_id, result_text)
    elif not no_moderators and not (is_chat_admin or is_chat_creator):
        er_text = await _('er_not_admin', lang=lang)
        result_text = f'"{text}":\n{er_text}'
        await send_message(chat_id, result_text)

    if (not no_moderators and is_chat_admin) or is_chat_creator:
        if not params:
            params = await get_redis_params(chat_id)

        command = text
        param = ADMIN_COMMANDS.get(command)

        value = params.get(param)

        if type(value) is str:
            if value.isdigit():
                value = int(value)

        if value == 0 or value == 1:
            value = int(value == 0)

        params.update({param: value})
        await put_redis_and_db_params(chat_id, params)

        keyboard_markup = await generate_settings_markup(chat_id=chat_id, lang=lang)

        result = await edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard_markup)


async def button_edit_handler(query: types.InlineQuery):
    # await print_handler(query, sys._getframe().f_code.co_name)

    if not 'message' in query:
        return

    message = query.message
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)
    user_id = query.from_user.id

    lang = params.get('LANGUAGE')
    bot = dp.bot

    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')

        return

    data = query.data
    if data == "language":
        lang_keyboard_markup = await generate_language_markup(chat_id=chat_id, lang=lang)

        # choose_language
        params = await get_redis_params(chat_id)

        lang = params.get('LANGUAGE')
        text = await _('choose_language', lang=lang)

        await send_message(chat_id=chat_id, text=text, reply_markup=lang_keyboard_markup)


async def button_language_handler(query: types.InlineQuery, callback_data: dict):
    # await print_handler(query, sys._getframe().f_code.co_name)

    if not 'message' in query:
        return

    lang = callback_data.get('lang')
    chat_id = int(callback_data.get('chat_id'))
    user_id = query.from_user.id
    bot = dp.bot

    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')
        return

    params = await get_redis_params(chat_id)
    params.update({'LANGUAGE': lang})
    await put_redis_and_db_params(chat_id, params)

    message_id = query.message.message_id
    text = await _('choose_language', lang=lang)

    lang_keyboard_markup = await generate_language_markup(chat_id=chat_id, lang=lang)
    await edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=lang_keyboard_markup)


async def button_not_bot_handler(query: types.InlineQuery, callback_data: dict):
    # await print_handler(query, sys._getframe().f_code.co_name)

    if not 'message' in query:
        return
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    checking_user_id = int(callback_data.get('user_id'))
    bot = dp.bot

    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    if is_chat_admin:
        return

    if user_id != checking_user_id:
        return

    button = callback_data.get('button')
    not_user_buttons = ('captcha_bot_button', 'captcha_not_user_button')
    message_id = query.message.message_id
    if button in not_user_buttons:
        msg = await send_message(chat_id=chat_id, text='sorry')
        await asyncio.sleep(3)

        await kick_chat_member(chat_id=chat_id, user_id=checking_user_id, until_date=td(minutes=5),
                               revoke_messages=True)
        await delete_message(chat_id=chat_id, message_id=msg.message_id)

    elif button == 'captcha_user_button':
        await restrict_chat_member(chat_id=chat_id, user_id=checking_user_id, can_send_messages=True,
                                   can_send_media_messages=True, can_send_other_messages=True,
                                   can_add_web_page_previews=True)

    await delete_message(chat_id=chat_id, message_id=message_id)
