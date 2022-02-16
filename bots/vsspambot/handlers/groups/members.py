import sys
from datetime import datetime as dt

from bots.vsspambot.data.localizations import commands_descriptions
from bots.vsspambot.keyboards.inline.guardian_keyboard import generate_confirm_markup
from bots.vsspambot.loader import dp, db
from bots.vsspambot.utils.bases import get_redis_params, get_redis_quarantine, put_redis_quarantine
from bots.vsspambot.utils.manage import send_message, print_handler, restrict_chat_member, get_lang_text

_ = get_lang_text


async def left_chat_member(message):
    await print_handler(message, sys._getframe().f_code.co_name)
    pass


async def new_member_handler(message):
    await print_handler(message, sys._getframe().f_code.co_name)

    bot = dp.bot
    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')
    no_captcha = params.get('NO_CAPTCHA')

    time_now = dt.now()
    for member in message.new_chat_members:

        is_bot = member.is_bot
        user_id = member.id
        username = member.username
        user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        is_chat_admin = user.is_chat_admin()

        if is_bot:
            me = await bot.me
            if user_id == me.id:
                text_list = list()
                if not is_chat_admin:
                    text = await _('er_bot_not_admin', lang=lang)
                    text_list.append(f"{text}\n")

                text = await _('commands', lang=lang)
                text_list.append(f"{text}:")

                command_list = commands_descriptions.get(lang)
                for command, desc in command_list.items():
                    text_list.append(f"/{command} — {desc}")
                text = '\n'.join(text_list)
                await send_message(chat_id=chat_id, text=text)

        else:

            first_name = member.first_name
            last_name = member.last_name
            if not first_name:
                first_name = username

            botusers = db.get('botusers')

            await botusers.add(username=username, first_name=first_name, last_name=last_name, user_id=str(user_id),
                               chat_id=str(chat_id))

            if is_chat_admin:
                continue

            if not no_captcha:
                await restrict_chat_member(chat_id=chat_id, user_id=user_id, can_send_messages=False)

                keyboard_markup = await generate_confirm_markup(user_id=user_id, lang=lang)
                text = await _('button_warning', lang=lang)
                await send_message(chat_id, f'{first_name}{text}', reply_markup=keyboard_markup)

            quarantine_users_dict = await get_redis_quarantine(chat_id)
            quarantine_users_dict.update({str(user_id): time_now.isoformat()})
            await put_redis_quarantine(chat_id=chat_id, users=quarantine_users_dict)
