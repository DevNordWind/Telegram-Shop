import json

from adaptix import Retort
from redis.asyncio import Redis

from .abstract import Repository
from ..models import RedisUser
from ...db.enums import Lang, Role, Currency


class UserRepo(Repository[RedisUser]):

    def __init__(self, redis: Redis, retort: Retort):
        super().__init__(type_model=RedisUser, redis=redis, retort=retort)

    async def new(self,
                  user_id: int | str,
                  id: int,
                  first_name: str,
                  role: Role,
                  currency: Currency,
                  lang: Lang | None = None,
                  username: str | None = None,
                  last_name: str | None = None,
                  ) -> RedisUser:
        user = RedisUser(
            id=id,
            first_name=first_name,
            currency=currency,
            role=role,
            lang=lang,
            username=username,
            last_name=last_name
        )
        await self.redis.set(user.build_key(user_id), value=json.dumps(user.__dict__))
        return user

    async def get_all_users(self) -> list[RedisUser]:
        keys = await self.redis.keys('user:*')
        return [await self.get_by_key(key) for key in keys]
