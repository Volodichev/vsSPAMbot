from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatType, Message

channel_types = [ChatType.CHANNEL]


class IsChannel(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type in channel_types
