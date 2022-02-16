from sqlalchemy import (
    Column, String, DateTime, MetaData, func, UniqueConstraint, Boolean
)

from apps.db.models.base import BaseModel, convention
from apps.users.db.models import BaseTelegramUserDB
from bots.vsspambot.data.config import DEFAULT_PARAMS

metadata = MetaData(naming_convention=convention)

#v. 0.1.14 15.02.2022


class VsSpamBotUserDB(BaseTelegramUserDB):
    """Model for vsspambot users"""
    __tablename__ = 'vsspambot_users'
    __tableargs__ = {'comment': 'Пользователи vsspambot'}

    # Schema
    chat_id = Column('chat_id', String)
    last_join_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    blocked = Column(Boolean, nullable=True, default=False)

    __table_args__ = (UniqueConstraint('user_id', 'chat_id', name='userchat_constraint'),)

    async def add(self, **kwargs):
        if 'values' in kwargs:
            start = 1
            part_values = []
            keys = kwargs['keys']

            params = []
            for kwargs_elem in kwargs['values']:
                params.extend(kwargs_elem)
                p_values = [f'${n}' for n, v in enumerate(kwargs_elem, start=start)]
                part_values.append('(' + ", ".join(p_values) + ')')
                start += len(keys)
            values = ', '.join(part_values)
        else:
            keys = [f"{k}" for k in kwargs]
            params = [v for v in kwargs.values()]
            part_values = [f'${n}' for n, v in enumerate(list(kwargs.values()), start=1)]
            values = '(' + ", ".join(part_values) + ')'

        # on_conflict = " ON CONFLICT (id) DO NOTHING"
        on_conflict = " ON CONFLICT ON CONSTRAINT userchat_constraint DO UPDATE SET " \
                      "username = EXCLUDED.username," \
                      "first_name = EXCLUDED.first_name," \
                      "last_name = EXCLUDED.last_name," \
                      "updated_at = CURRENT_TIMESTAMP," \
                      "last_join_date = GREATEST(EXCLUDED.last_join_date, CURRENT_TIMESTAMP)"

        query_list = list()
        query_list.append(f"INSERT INTO {self.__tablename__} (")
        query_list.append(", ".join(keys))
        query_list.append(") VALUES ")
        query_list.append(values)
        query_list.append(on_conflict)
        query_list.append(";")

        query = "".join(query_list)

        return await self.execute(query, params=tuple(params), commit=True)


class VsSpamBotSettings(BaseModel):
    """Model for bot settings vsspambot"""
    __tablename__ = 'vsspambot_settings'
    __tableargs__ = {'comment': 'Параметры vsspambot'}

    # Schema
    chat_id = Column('chat_id', String, nullable=False, unique=True)  # -1001354199969
    params = Column('params', String, nullable=False, server_default=str(DEFAULT_PARAMS))

    async def add(self, **kwargs):
        if 'values' in kwargs:
            start = 1
            part_values = []
            keys = kwargs['keys']

            params = []
            for kwargs_elem in kwargs['values']:
                params.extend(kwargs_elem)
                p_values = [f'${n}' for n, v in enumerate(kwargs_elem, start=start)]
                part_values.append('(' + ", ".join(p_values) + ')')
                start += len(keys)
            values = ', '.join(part_values)
        else:
            keys = [f"{k}" for k in kwargs]
            params = [v for v in kwargs.values()]
            part_values = [f'${n}' for n, v in enumerate(list(kwargs.values()), start=1)]
            values = '(' + ", ".join(part_values) + ')'

        # on_conflict = " ON CONFLICT (id) DO NOTHING"
        on_conflict = " ON CONFLICT (chat_id) DO UPDATE SET " \
                      "params = EXCLUDED.params," \
                      "updated_at = CURRENT_TIMESTAMP"

        query_list = list()
        query_list.append(f"INSERT INTO {self.__tablename__} (")
        query_list.append(", ".join(keys))
        query_list.append(") VALUES ")
        query_list.append(values)
        query_list.append(on_conflict)
        query_list.append(";")

        query = "".join(query_list)

        return await self.execute(query, params=tuple(params), commit=True)

