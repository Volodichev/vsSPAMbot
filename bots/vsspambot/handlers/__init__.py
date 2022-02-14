import logging

from bots.vsspambot.loader import dp
from .callbacks import register_handlers_buttons
from .common import register_errors
from .groups import *
from .users import register_handlers_users_info, register_handlers_users_text

if __name__ == "bots.vsspambot.handlers":
    register_errors(dp)
    register_handlers_buttons(dp)

    register_handlers_admins(dp)
    register_handlers_antispam(dp)
    register_handlers_members(dp)
    register_handlers_text(dp)

    register_handlers_users_info(dp)
    register_handlers_users_text(dp)

    logging.info("Handlers are successfully configured")
