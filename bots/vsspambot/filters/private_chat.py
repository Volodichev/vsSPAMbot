from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatType, Message

chat_types_private = [ChatType.PRIVATE]


class IsPrivate(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type in chat_types_private
