from abc import ABCMeta, abstractmethod

from seed_work.entities import Entity


class GenericRepository(metaclass=ABCMeta):
    model = None

    @abstractmethod
    async def get_by_id(self, _id: int) -> Entity:
        ...

    @abstractmethod
    async def insert(self, entity: Entity):
        ...

    @abstractmethod
    async def update(self, entity: Entity):
        ...

    async def delete_by_id(self, _id: int):
        ...
