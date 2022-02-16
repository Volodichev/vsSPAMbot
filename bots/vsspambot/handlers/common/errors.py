import logging
import sys

from aiogram import types
from aiogram.utils.exceptions import (BotBlocked, Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)

from bots.vsspambot.utils.bases import get_redis_params
from bots.vsspambot.utils.manage import send_message, get_lang_text, print_handler

_ = get_lang_text


async def error_command_private_handler(message: types.Message):
    await print_handler(message, sys._getframe().f_code.co_name)

    chat_id = message.chat.id
    params = await get_redis_params(chat_id)
    lang = params.get('LANGUAGE')

    er_text = await _('only_in_chats', lang=lang)

    await send_message(chat_id, er_text)


async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    logging.debug(f"Bot is blocked by user!\nupdate: {update}\nerror: {exception}")
    return True


async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    logging.exception(f'Update: {update} \n{exception}')
