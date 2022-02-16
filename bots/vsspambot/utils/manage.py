import asyncio
import logging
import re
import typing
from aiogram.types import ParseMode, Message
from aiogram.utils import exceptions

from bots.vsspambot.loader import bot, dp
from bots.vsspambot.data.localizations import localizations


async def print_handler(message, name='message'):
    message = str(message).replace("false", "False").replace("true", "True")
    logging.debug(f'{name} = {message.encode("utf-8")}\n')


async def send_message(chat_id: int, text: str, parse_mode=ParseMode.HTML, disable_notification: bool = False,
                       reply_markup=None, disable_web_page_preview=None) -> bool or Message:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    result = False
    try:
        result = await bot.send_message(chat_id=chat_id, text=text, disable_notification=disable_notification,
                                        parse_mode=parse_mode, reply_markup=reply_markup,
                                        disable_web_page_preview=disable_web_page_preview)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{chat_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{chat_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(chat_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{chat_id}]: failed")
    except Exception as e:
        logging.exception(f"Unknown exception: {e}")
    else:
        logging.debug(f"Target [ID:{chat_id}]: success")
    return result


async def delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except exceptions.MessageToDeleteNotFound:
        logging.error(f"Message to delete very old or deleted or unknown message")
    except exceptions.MessageCantBeDeleted:
        logging.error(f"message can\'t be deleted")
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.BotBlocked:
        logging.exception(f"bot was blocked by the user")
    except exceptions.BotKicked:
        logging.exception(f"bot was kicked from")
    except exceptions.ChatNotFound:
        logging.exception(f"chat not found")
    except exceptions.MessageError:
        logging.exception(f"MessageError")
    except Exception as e:
        logging.exception(f"Unknown exception: {e}")
    else:
        logging.debug(f"delete message:{message_id}]: success")
        return True
    return False


async def edit_message_reply_markup(chat_id: int, message_id: int, reply_markup=None, **kwargs):
    try:
        return await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup,
                                                   **kwargs)
    except:
        pass


async def edit_message_text(text: str, chat_id: int, message_id: int, reply_markup=None, **kwargs):
    try:
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup,
                                    **kwargs)
    except:
        pass


async def delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass


async def kick_chat_member(chat_id: int, user_id: int, until_date=None, revoke_messages=None):
    try:
        await bot.kick_chat_member(chat_id=chat_id, user_id=user_id, until_date=until_date,
                                   revoke_messages=revoke_messages)
    except Exception as e:
        print(f'kick_chat_member: {e}')
        pass


async def unban_chat_member(chat_id: int, user_id: int, **kwargs):
    try:
        await bot.unban_chat_member(chat_id=chat_id, user_id=user_id, **kwargs)
    except:
        pass


async def restrict_chat_member(chat_id: int, user_id: int, **kwargs):
    try:
        await bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, **kwargs)

    except:
        pass


async def promote_chat_member(
        chat_id: typing.Union[int, str],
        user_id: int, **kwargs):
    try:
        await bot.promote_chat_member(chat_id=chat_id, user_id=user_id, **kwargs)

    except:
        pass


async def is_bot_admin(chat_id):
    bot = dp.bot
    me = await bot.me
    user_bot = await bot.get_chat_member(chat_id=chat_id, user_id=me.id)
    return user_bot.is_chat_admin()


async def get_commands(message) -> dict:
    """
    Get commands from message

    :return: dict
    """
    commands = dict()
    prev_command = None
    for text_part in message.text.split():
        if '@' in text_part:
            for text_command in [s.replace('@', '') for s in re.findall(r'\/.+@', text_part)]:
                commands.update({text_command: None})
                prev_command = text_command
        elif text_part.startswith("/"):
            commands.update({text_part: None})
            prev_command = text_part
        else:
            if prev_command:
                commands.update({prev_command: text_part})
                prev_command = ''

    return commands


async def get_lang_text(lang_text=None, lang='en'):
    if lang_text:
        lang_texts = localizations.get(lang_text)
        lang_text = lang_texts.get(lang, None)
        if lang_text is None:
            lang_text = lang_texts.get('en')

    return lang_text
