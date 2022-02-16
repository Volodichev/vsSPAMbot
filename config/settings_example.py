import os

# POSTGRES
PGUSER = os.getenv("PGUSER", default="restapi_user").strip()
PGPASS = os.getenv("PGPASS").strip()

PGDATABASE = os.getenv("PGDATABASE", default="restapi").strip()
PGHOST = os.getenv("PGHOST", default="localhost").strip()
PGPORT = os.getenv("PGPORT", default='5432').strip()

# SSL and CERTS
SSL = os.getenv("SSL").strip()
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", default=None).strip()

# BOTS and TOKENS
BOT_TOKENS = eval(os.getenv("BOT_TOKENS").strip())

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", default="localhost").strip()  # 'localhost:6379'
REDIS_PORT = os.getenv("REDIS_PORT", default=6379).strip()
REDIS_PASS = os.getenv("REDIS_PASS", default='').strip()
