import os
from config.settings import BOT_TOKENS, WEBHOOK_HOST, REDIS_HOST, REDIS_PORT, REDIS_PASS

# BASE_URL = os.getenv("BASE_URL").strip()
# WEBHOOK_PATH = f'{BOT_TOKEN}/tgbot'
# WEBHOOK_URL = f'{BASE_URL}/{WEBHOOK_PATH}/'
# ssl_path = os.getenv("SSL_PATH").strip()

# POSTGRES
# PGUSER = os.getenv("PGUSER").strip()
# PGPASS = os.getenv("PGPASS").strip()
#
# DATABASE = os.getenv("DATABASE").strip()
# PGHOST = os.getenv("PGHOST").strip()

# SSL and CERTS
# SSL = ''
# WEBHOOK_HOST = ''

# BOTS and TOKENS
# BOT_NAME = 'vsspambot'
BOT_NAME = 'test_vsspambot'
# BOT_TOKENS = eval(os.getenv("BOT_TOKENS").strip())
BOT_TOKEN = BOT_TOKENS.get(BOT_NAME, None)

# REDIS
# REDIS_HOST = os.getenv("REDIS_HOST").strip()
# REDIS_PORT = os.getenv("REDIS_PORT").strip()
# REDIS_PASS = os.getenv("REDIS_PASS").strip()
BOT_REDIS_QUARANTEEN_USERS = f'{BOT_NAME}:users'
BOT_REDIS_CONFIG = f'{BOT_NAME}:config'

# WEBHOOK
WEBHOOK_PATH = f'/bot?name={BOT_NAME}&token={BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
REDIS_PARAMS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASS
}



# JOIN_CONFIRM_DURATION = datetime.timedelta(minutes=2)
# JOIN_NO_MEDIA_DURATION = datetime.timedelta(minutes=2)
# SUPERUSER_IDS = env.list("SUPERUSER_IDS")
#
# SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
# NUM_BUTTONS = env.int("NUM_BUTTONS", 5)
# ENTRY_TIME = env.int("ENTRY_TIME", 300)
# BAN_TIME = env.int("BAN_TIME", 30)
#
# WORK_PATH = os.getcwd()

# BOT DICTS
ADMIN_COMMANDS = {
    '/no_link': 'NO_LINK',
    '/no_repost': 'NO_REPOST',
    '/no_uname': 'NO_USERNAME',
    '/no_email': 'NO_EMAIL',
    '/no_sticker': 'NO_STICKER',
    '/no_doc': 'NO_DOC',
    '/no_photo': 'NO_PHOTO',
    '/no_audio': 'NO_AUDIO',
    '/no_video': 'NO_VIDEO',
    '/no_vidnote': 'NO_VIDEONOTE',
    '/no_gif': 'NO_ANIMATION',
    '/no_poll': 'NO_POLL',
    '/no_voice': 'NO_VOICE',
    '/no_fword': 'NO_FWORD',
    '/no_captcha': 'NO_CAPTCHA',
    '/readonly': 'READONLY'
}
CREATOR_COMMANDS = {
    '/no_admins': 'NO_ADMINS'
}
EDIT_COMMANDS = {
    '/language': 'LANGUAGE',
    '/quarantine': 'QUARANTINE'
}
DEFAULT_PARAMS = {
    'NO_LINK': 0,
    'NO_REPOST': 0,
    'NO_USERNAME': 0,
    'NO_EMAIL': 0,
    'NO_STICKER': 0,
    'NO_DOC': 0,
    'NO_PHOTO': 0,
    'NO_AUDIO': 0,
    'NO_VIDEO': 0,
    'NO_VIDEONOTE': 0,
    'NO_ANIMATION': 0,
    'NO_POLL': 0,
    'NO_VOICE': 0,
    'NO_FWORD': 0,
    'NO_ADMINS': 0,
    'NO_CAPTCHA': 0,
    'LANGUAGE': 'en',
    'READONLY': 0,
    'QUARANTINE': 24,
}

flags = {
    'en': '🇬🇧',
    'ru': '🇷🇺',
    'it': '🇮🇹',
    'et': '🇪🇪',
    'uk': '🇺🇦',
    'pt': '🇵🇹',
    'tr': '🇹🇷',
    'es': '🇪🇸',
    'zh': '🇨🇳',
    'no': '🇳🇴',
    'de': '🇩🇪',
    'tw': '🇹🇼',
    'fr': '🇫🇷',
    'id': '🇮🇩',
    'ko': '🇰🇷',
    'am': '🇪🇹',
    'cz': '🇨🇿',
    'sk': '🇸🇰',
    'ar': '🇦🇪',
    'ja': '🇯🇵',
    'ro': '🇷🇴',
    'ca': '🏳️',
    'he': '🇮🇱',
    'hu': '🇭🇺',
    'fi': '🇫🇮',
    'kz': '🇰🇿',
    'bg': '🇧🇬'
}
langs = {
    'English': 'en',
    'Русский': 'ru',
    'Italiano': 'it',
    'Eesti': 'et',
    'Українська': 'uk',
    'Português': 'pt',
    'Español': 'es',
    'Chinese': 'zh',
    'Norwegian': 'no',
    'Deutsch': 'de',
    'Taiwan': 'tw',
    'French': 'fr',
    'Indonesian': 'id',
    'Korean': 'ko',
    'Amharic': 'am',
    'Czech': 'cz',
    'Arabic': 'ar',
    'Türkçe': 'tr',
    'Romanian': 'ro',
    'Japanese': 'ja',
    'Slovak': 'sk',
    'Catalan': 'ca',
    'עברית': 'he',
    'Hungarian': 'hu',
    'Finnish': 'fi',
    'Қазақ': 'kz',
    'Bulgarian': 'bg'
}
spam_content_types = (
    "video",
    "audio",
    "photo",
    "video_note",
    "voice",
    "sticker",
    "sticker_set",
    "document",
    "animation",
    "poll",
)
