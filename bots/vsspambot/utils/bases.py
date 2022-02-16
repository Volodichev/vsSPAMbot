import datetime
import json
from datetime import datetime as dt, timedelta as td

import aioredis

from bots.vsspambot.data.config import (ADMIN_COMMANDS, CREATOR_COMMANDS, EDIT_COMMANDS, DEFAULT_PARAMS, flags,
                                        BOT_REDIS_QUARANTEEN_USERS, BOT_REDIS_CONFIG, REDIS_HOST, REDIS_PORT, REDIS_PASS)
from bots.vsspambot.loader import db

time_now = datetime.datetime.now()
redis_uri = f"redis://{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}" if REDIS_PASS else f"redis://{REDIS_HOST}:{REDIS_PORT}"
# redis_uri = f"redis://localhost:6379"
redis_storage = aioredis.from_url(redis_uri)

async def get_keys_redis():
    redis_keys = await redis_storage.keys()
    return redis_keys


async def clean_redis():
    redis_keys = await get_keys_redis()
    for redis_key in redis_keys:
        result = await redis_storage.delete(redis_key)
        print(f'удалено {redis_key}: {result}')


async def get_from_redis(key):
    if not key:
        print(f'error get_from_redis {key=}')
        return None
    redis_str = await redis_storage.get(key)
    return redis_str

async def json_loads_params(params_json=None):
    try:
        params = json.loads(params_json) if params_json else DEFAULT_PARAMS
    except:
        params = DEFAULT_PARAMS

    return params

async def json_loads_quarantine_users(qud_json=None):
    try:
        quarantine_users_dict = json.loads(qud_json) if qud_json else dict()
    except:
        quarantine_users_dict = dict()

    return quarantine_users_dict

async def get_redis_params(chat_id):
    key = f"{BOT_REDIS_CONFIG}:{chat_id}"
    params_json = await get_from_redis(key)

    params = await json_loads_params(params_json)

    if params.get('null'):
        params.pop('null')

    return params


async def get_redis_quarantine(chat_id):
    """
    ATTENTION USE JSON isoformat for dates
    # time_now_iso = time_now.isoformat()
    # time_now = datetime.datetime.fromisoformat(time_now_iso)
    """
    key = f"{BOT_REDIS_QUARANTEEN_USERS}:{chat_id}"
    qud_json = await get_from_redis(key)
    quarantine_users_dict = await json_loads_quarantine_users(qud_json)

    return quarantine_users_dict


async def put_to_redis(key, value):
    result = await redis_storage.set(key, value)
    return result


async def put_redis_params(chat_id, params):
    key = f"{BOT_REDIS_CONFIG}:{chat_id}"
    return await put_to_redis(key, json.dumps(params))


async def put_redis_and_db_params(chat_id, params):
    await put_redis_params(chat_id, params)
    botsets = db.get('botsets')
    await botsets.add(chat_id=str(chat_id), params=json.dumps(params))


async def put_redis_params_pipe(chat_params):
    async with redis_storage.pipeline(transaction=True) as pipe:
        for chat_id, params in chat_params.items():
            key = f"{BOT_REDIS_CONFIG}:{chat_id}"
            params_json = json.dumps(params)
            result = await pipe.set(key, params_json)
        result = await pipe.execute()

    return result


async def put_redis_quarantine(chat_id, users):
    key = f"{BOT_REDIS_QUARANTEEN_USERS}:{chat_id}"
    return await put_to_redis(key, json.dumps(users))


async def init_bases_params():
    base = db.get('base')
    botusers = db.get('botusers')
    botsets = db.get('botsets')

    await base.create_pool()
    botusers.pool = base.pool
    botsets.pool = base.pool
    db.update({'base': base, 'botusers': botusers, 'botsets': botsets})

    chat_quarantine_timers = {}
    quarantine_max = 24

    sets_list = await botsets.select()
    for sets in sets_list:
        chat_id = sets.get('chat_id')
        params_json = sets.get('params')
        # params = json.loads(params_json) if params_json else DEFAULT_PARAMS
        params = await json_loads_params(params_json)
        new_params = DEFAULT_PARAMS
        new_params.update(params)
        params = new_params

        await put_redis_params(chat_id, params)

        quarantine_time = int(params.get('QUARANTINE'))
        quarantine_max = max(quarantine_time, quarantine_max)
        chat_quarantine_timers.update({chat_id: quarantine_time})

    quarantine_chats = {}
    quarantine_user_list = await botusers.select(last_join_date__EQLESS=dt.now() - td(hours=int(quarantine_max)),
                                                 sort=['chat_id'])

    for quarantine_user in quarantine_user_list:
        chat_id = quarantine_user.get('chat_id')
        last_join_date = quarantine_user.get('last_join_date')  # timestamp
        quarantine_time = chat_quarantine_timers.get(chat_id, quarantine_max)

        if last_join_date >= dt.now() - td(hours=quarantine_time):
            user_id = quarantine_user.get('user_id')
            last_join_date_iso = last_join_date.isoformat()

            quarantine_users_dict = quarantine_chats.get(chat_id, dict())
            quarantine_users_dict.update({user_id: last_join_date_iso})
            quarantine_chats.update({chat_id: quarantine_users_dict})

    for quarantine_chat_id, quarantine_users_dict in quarantine_chats.items():
        await put_redis_quarantine(quarantine_chat_id, quarantine_users_dict)


async def get_params_commands(chat_id):
    params = await get_redis_params(chat_id)

    param_dict = dict()
    commands = ADMIN_COMMANDS
    commands.update(CREATOR_COMMANDS)
    commands.update(EDIT_COMMANDS)

    commands_keys = list(commands.keys())
    commands_values = list(commands.values())
    for key, value in params.items():
        if not key or key == 'null':
            continue

        command = commands_keys[commands_values.index(key)]
        status = f'{value}'

        if type(value) is str:
            if value.isdigit():
                value = int(value)
            elif value.isalpha():
                status = flags.get(value)

        if value == 0 or value == 1:
            status = '✅' if value else '❌'

        param_dict.update({f'{command}: {status}': command[1:]})

    return param_dict
