import sys

from aiogram.types import Message

from bots.vsspambot.data.config import ADMIN_COMMANDS, CREATOR_COMMANDS, EDIT_COMMANDS
from bots.vsspambot.keyboards.inline.settings_keyboard import generate_language_markup, generate_settings_markup
from bots.vsspambot.loader import dp
from bots.vsspambot.utils.bases import get_redis_params, get_params_commands, put_redis_and_db_params
from bots.vsspambot.utils.manage import send_message, print_handler, is_bot_admin, get_commands, get_lang_text
from bots.vsspambot.utils.throttling import rate_limit

_ = get_lang_text


async def command_creator_handler(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    bot = dp.bot
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    user_id = message.from_user.id
    text = message.text
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_creator = user.is_chat_creator()
    if not is_chat_creator:
        er_text = await _('er_not_creator', lang=lang)
        er_text = f'"{text}":\n{er_text}'

        await send_message(chat_id, er_text)

    else:

        params = await get_redis_params(chat_id)

        commands = await get_commands(message)
        for command, parametr in commands.items():
            param = CREATOR_COMMANDS.get(command)
            res = int(params.get(param) == 0)

            params.update({param: res})
            await put_redis_and_db_params(chat_id, params)

            status = '✅' if res else '❌'
            result_text = f'{text}: {status}'

            await send_message(chat_id, result_text)


async def command_admin_handler(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    params = None
    result_text = None
    no_moderators = None

    bot = dp.bot
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')

    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)

        await send_message(chat_id, er_text)
        return

    user_id = message.from_user.id
    text = message.text
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    is_chat_creator = user.is_chat_creator()
    sender_chat = message.sender_chat
    if sender_chat:
        if chat_id == sender_chat.id:
            # logic to anonim admin user
            is_chat_admin = True

    if is_chat_creator or is_chat_admin:
        params = await get_redis_params(chat_id)
        no_moderators = params.get('NO_MODERATORS')

    if no_moderators and not is_chat_creator:
        er_text = await _('er_not_creator', lang=lang)
        result_text = f'"{text}":\n{er_text}'
    elif not no_moderators and not (is_chat_admin or is_chat_creator):
        er_text = await _('er_not_admin', lang=lang)
        result_text = f'"{text}":\n{er_text}'

    if (not no_moderators and is_chat_admin) or is_chat_creator:
        if not params:
            params = await get_redis_params(chat_id)

        commands = await get_commands(message)
        for command, parametr in commands.items():
            param = ADMIN_COMMANDS.get(command)
            res = int(params.get(param) == 0)
            params.update({param: res})

            await put_redis_and_db_params(chat_id, params)

            status = '✅' if res else '❌'
            result_text = f'{text}: {status}'

    if result_text:
        await send_message(chat_id, result_text)


async def command_quarantine_handler(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    bot = dp.bot
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    user_id = message.from_user.id
    text = message.text
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

    is_chat_admin = user.is_chat_admin()

    sender_chat = message.sender_chat
    if sender_chat:
        if chat_id == sender_chat.id:
            # logic to anonim admin user
            is_chat_admin = True

    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')
    else:
        commands = await get_commands(message)
        params = await get_redis_params(chat_id)

        for command, parametr in commands.items():
            param = EDIT_COMMANDS.get(command)
            old_parametr = params.get(param)

            if not (parametr and parametr.isnumeric()):

                text = await _('prohibition_time', lang=lang)
                await send_message(chat_id, f'{text}\n\"{command} {old_parametr}\"')
            else:
                params.update({param: parametr})

                await put_redis_and_db_params(chat_id, params)

                result_text = f'{command}: {parametr}ч.'
                await send_message(chat_id, result_text)


async def command_info_handler(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)
    user_id = message.from_user.id

    lang = params.get('LANGUAGE')

    if not await is_bot_admin(chat_id):
        er_text = await _('er_bot_not_admin', lang=lang)
        await send_message(chat_id, er_text)
        return

    bot = dp.bot
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()

    sender_chat = message.sender_chat
    if sender_chat:
        if chat_id == sender_chat.id:
            # logic to anonim admin user
            is_chat_admin = True

    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')
        return

    text = await _('configuration', lang=lang)
    text_list = [f"{text}:"]
    p = await get_params_commands(chat_id=chat_id)
    text_list.extend(list(p.keys()))

    text_list.append(f'/settings\nhelp: <a href="https://t.me/vsspambot?start">/help</a>')
    text = '\n'.join(text_list)
    await send_message(chat_id=chat_id, text=text)


async def show_params_buttons(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    chat_id = message.chat.id
    user_id = message.from_user.id

    bot = dp.bot
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()
    params = await get_redis_params(chat_id)
    lang = params.get('LANGUAGE')

    sender_chat = message.sender_chat
    if sender_chat:
        if chat_id == sender_chat.id:
            # logic to anonim admin user
            is_chat_admin = True

    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')

        return

    keyboard_markup = await generate_settings_markup(chat_id=chat_id)

    text = await _('configuration', lang=lang)
    await send_message(chat_id, text=f"{text}: \n",
                       reply_markup=keyboard_markup,
                       disable_web_page_preview=True
                       )


@rate_limit(3, 'language')
async def show_language_buttons(message: Message):
    # await print_handler(message, sys._getframe().f_code.co_name)

    chat_id = message.chat.id
    user_id = message.from_user.id
    params = await get_redis_params(chat_id)

    bot = dp.bot
    user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    is_chat_admin = user.is_chat_admin()

    lang = params.get('LANGUAGE')

    sender_chat = message.sender_chat
    if sender_chat:
        if chat_id == sender_chat.id:
            is_chat_admin = True

    if not is_chat_admin:
        er_text = await _('er_not_admin', lang=lang)
        await send_message(chat_id, f'{er_text}')
        return

    commands = await get_commands(message)
    for command, parametr in commands.items():
        if parametr:
            lang = parametr

            params.update({'LANGUAGE': lang})

            await put_redis_and_db_params(chat_id, params)

            return

    keyboard_markup = await generate_language_markup(chat_id=chat_id, lang=lang)

    await send_message(chat_id, text=await _('choose_language', lang=lang), reply_markup=keyboard_markup)
