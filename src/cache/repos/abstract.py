import abc
import json
from typing import TypeVar, Generic, Any

from adaptix import Retort
from redis.asyncio import Redis

AbstractModel = TypeVar('AbstractModel')
from ..models import Base


class Repository(Generic[AbstractModel]):
    """Repository abstract class."""

    type_model: type[Base]
    redis: Redis
    retort: Retort

    def __init__(self, type_model: type[Base], redis: Redis, retort: Retort):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        self.type_model = type_model
        self.redis = redis
        self.retort = retort

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        pass

    async def get_by_key(self, key: str) -> AbstractModel | None:
        if (r_query := await self.redis.get(key)) is None:
            return None

        data = json.loads(r_query)
        return self.retort.load(data, self.type_model)

    async def update_model(self, model: AbstractModel, key: Any = None) -> None:
        dumps = json.dumps(model.__dict__)
        await self.redis.set(self.type_model.build_key(key), dumps)