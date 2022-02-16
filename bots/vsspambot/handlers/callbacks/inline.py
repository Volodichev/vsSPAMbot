import asyncio
import sys
from datetime import timedelta as td

from aiogram.types import CallbackQuery

from bots.vsspambot.data.config import ADMIN_COMMANDS, CREATOR_COMMANDS, EDIT_COMMANDS
from bots.vsspambot.keyboards.inline.settings_keyboard import generate_language_markup, generate_settings_markup
from bots.vsspambot.loader import dp
from bots.vsspambot.utils.bases import get_redis_params, put_redis_and_db_params
from bots.vsspambot.utils.manage import (is_bot_admin, send_message, print_handler, edit_message_reply_markup,
                                         edit_message_text, delete_message, kick_chat_member, restrict_chat_member,
                                         get_lang_text, user_is_chat_admin, user_is_chat_creator)
from bots.vsspambot.utils.throttling import rate_limit

_ = get_lang_text


@rate_limit(3, 'params')
async def button_params_buttons(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')
    message = query.message
    if not message:
        return

    chat_id = message.chat.id
    # user_id = query.from_user.id
    # bot_id = message.from_user.id
    #
    # bot = dp.bot
    params = await get_redis_params(chat_id)
    lang = params.get('LANGUAGE')

    is_chat_admin = await user_is_chat_admin(query)
    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')

        return

    text = await _('configuration', lang=lang)
    keyboard_markup = await generate_settings_markup(chat_id=chat_id)
    if 'message_id' in message:
        message_id = query.message.message_id
        await edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=keyboard_markup)
    else:
        await send_message(chat_id, text=f"{text}: \n",
                           reply_markup=keyboard_markup,
                           disable_web_page_preview=True
                           )


async def button_creator_handler(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')

    message = query.message
    if not message:
        return

    if 'command' in callback_data:
        command = callback_data.get('command')
    else:
        return

    full_command = f'/{command}'

    bot = dp.bot
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    is_chat_creator = await user_is_chat_creator(query)
    if not is_chat_creator:
        er_text = await _('er_not_creator', lang=lang)
        er_text = f'"{full_command}":\n{er_text}'

        await send_message(chat_id, er_text)

    else:

        params = await get_redis_params(chat_id)

        param = CREATOR_COMMANDS.get(full_command)
        res = int(params.get(param) == 0)

        params.update({param: res})
        await put_redis_and_db_params(chat_id, params)

        status = '✅' if res else '❌'
        result_text = f'{full_command}: {status}'

        await send_message(chat_id, result_text)


async def button_admin_handler(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')
    message = query.message
    if not message:
        return

    if 'command' in callback_data:
        command = callback_data.get('command')
    else:
        return
    full_command = f'/{command}'

    no_admins = None
    message_id = message.message_id

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    is_chat_admin = await user_is_chat_admin(query)
    is_chat_creator = await user_is_chat_creator(query)

    if is_chat_creator or is_chat_admin:
        params = await get_redis_params(chat_id)
        no_admins = params.get('NO_ADMINS')

    if no_admins and not is_chat_creator:
        er_text = await _('er_not_creator', lang=lang)
        result_text = f'"{full_command}":\n{er_text}'
        await send_message(chat_id, result_text)
    elif not no_admins and not (is_chat_admin or is_chat_creator):
        er_text = await _('er_not_admin', lang=lang)
        result_text = f'"{full_command}":\n{er_text}'
        await send_message(chat_id, result_text)

    if (not no_admins and is_chat_admin) or is_chat_creator:
        if not params:
            params = await get_redis_params(chat_id)

        param = ADMIN_COMMANDS.get(full_command)

        value = params.get(param)

        if type(value) is str:
            if value.isdigit():
                value = int(value)

        if value == 0 or value == 1:
            value = int(value == 0)

        params.update({param: value})
        await put_redis_and_db_params(chat_id, params)

        keyboard_markup = await generate_settings_markup(chat_id=chat_id, message_id=message_id, lang=lang)

        result = await edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard_markup)


async def button_edit_handler(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')

    message = query.message
    if not message:
        return

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)
    lang = params.get('LANGUAGE')
    is_chat_admin = await user_is_chat_admin(query)
    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')
        return

    if 'command' in callback_data:
        command = callback_data.get('command')
        full_command = f'/{command}'

        if command == "language":
            # choose_language
            lang_keyboard_markup = await generate_language_markup(chat_id=chat_id, lang=lang)
            text = await _('choose_language', lang=lang)
            if 'message_id' in message:
                message_id = query.message.message_id

                await edit_message_text(text=text, chat_id=chat_id, message_id=message_id,
                                        reply_markup=lang_keyboard_markup)
            else:

                await send_message(chat_id=chat_id, text=text, reply_markup=lang_keyboard_markup)

        elif command == "quarantine":
            param = EDIT_COMMANDS.get(full_command)
            old_parametr = params.get(param)

            text = await _('prohibition_time', lang=lang)
            await send_message(chat_id, f'{text}\n\"{full_command} {old_parametr}\"')


async def button_language_handler(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')

    message = query.message
    if not message:
        return

    lang = callback_data.get('lang')
    chat_id = int(callback_data.get('chat_id'))
    is_chat_admin = await user_is_chat_admin(query)
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


async def button_not_bot_handler(query: CallbackQuery, callback_data: dict):
    await print_handler(query, sys._getframe().f_code.co_name)

    print(f'{callback_data=}')

    message = query.message
    if not message:
        return

    chat_id = query.message.chat.id
    user_id = query.from_user.id
    checking_user_id = int(callback_data.get('user_id'))
    is_chat_admin = await user_is_chat_admin(query)
    if is_chat_admin:
        return

    if user_id != checking_user_id:
        return

    button = callback_data.get('button')
    not_user_buttons = ('captcha_bot_button', 'captcha_not_user_button')
    message_id = message.message_id

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
