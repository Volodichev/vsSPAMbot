from bots.vsspambot.loader import dp
from .group_chat import ContainsMention, IsGroup, IsTestGroup
from .private_chat import IsPrivate
import logging

if __name__ == "bots.vsspambot.filters":
    dp.filters_factory.bind(ContainsMention)
    dp.filters_factory.bind(IsTestGroup)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    logging.info("Filters are successfully configured")
