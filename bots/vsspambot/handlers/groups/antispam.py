import sys
from datetime import datetime as dt, timedelta as td

from bots.vsspambot.utils.bases import get_redis_params, get_redis_quarantine
from bots.vsspambot.utils.manage import (send_message, delete_message, print_handler, get_lang_text, user_is_chat_admin)

_ = get_lang_text


async def custom_spam_handler(message):
    await print_handler(message, sys._getframe().f_code.co_name)

    time_now = dt.now()

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)

    lang = params.get('LANGUAGE')

    user_id = message.from_user.id

    if await user_is_chat_admin(message):
        return True

    username = message.from_user.first_name
    if not username:
        username = "User"
    message_id = message.message_id
    params = await get_redis_params(chat_id)

    if message.forward_from_chat and params.get('NO_REPOST'):
        await delete_message(chat_id=chat_id, message_id=message_id)

    for ent in message.entities:
        ent_type = ent.type
        if ent_type in ('url', 'text_link'):
            if params.get('NO_LINK'):
                await delete_message(chat_id=chat_id, message_id=message_id)

        if ent_type == 'mention':
            text = message.text
            if text.statrtswith('@'):
                if params.get('NO_USERNAME'):
                    await delete_message(chat_id=chat_id, message_id=message_id)

        if ent_type in ('email') and params.get('NO_EMAIL'):
            await delete_message(chat_id=chat_id, message_id=message_id)

    quarantine_users_dict = await get_redis_quarantine(chat_id)
    quarantine_time = int(params.get('QUARANTINE'))

    if str(user_id) in quarantine_users_dict.keys():
        last_join_date_iso = quarantine_users_dict.get(str(user_id))
        last_join_date = dt.fromisoformat(last_join_date_iso)

        if last_join_date + td(hours=quarantine_time) > time_now:
            await delete_message(chat_id=chat_id, message_id=message_id)

            text = await _('links_forbidden', lang=lang)
            text = text.format(quarantine_time=quarantine_time)
            await send_message(chat_id, f'{username},\n{text}')


async def spam_handler(message):
    await print_handler(message, sys._getframe().f_code.co_name)

    chat_id = message.chat.id
    message_id = message.message_id
    content_type = message.content_type

    if await user_is_chat_admin(message):
        return True

    params = await get_redis_params(chat_id)

    if content_type in ["video"] and params.get('NO_VIDEO'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["audio"] and params.get('NO_AUDIO'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["photo"] and params.get('NO_PHOTO'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["video_note"] and params.get('NO_VIDEONOTE'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["voice"] and params.get('NO_VOICE'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["sticker", "sticker_set"] and params.get('NO_STICKER'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["document"] and params.get('NO_DOC'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["animation"] and params.get('NO_ANIMATION'):
        await delete_message(chat_id=chat_id, message_id=message_id)
    if content_type in ["poll"] and params.get('NO_POLL'):
        await delete_message(chat_id=chat_id, message_id=message_id)
