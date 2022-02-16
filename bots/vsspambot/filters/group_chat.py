from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatType, Message

from config.settings import TEST_CHAT_IDS

chat_types_group = [ChatType.GROUP, ChatType.SUPERGROUP]


class IsTestGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        chat = message.chat
        return chat.type in chat_types_group and str(chat.id) in TEST_CHAT_IDS


class ContainsMention(BoundFilter):
    async def check(self, message: Message) -> bool:
        if message.chat.type in chat_types_group:
            if message.forward_from_chat:
                return True

            entities = message.entities
            for ent in entities:
                ent_type = ent.type
                if ent_type in ('url', 'text_link'):
                    return True

                if ent_type == 'mention':
                    text = message.text
                    if text.statrtswith('@'):
                        return True

                if ent_type in ('email',):
                    return True

        return False


class IsGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type in chat_types_group