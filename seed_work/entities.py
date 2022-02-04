from typing import Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: Optional[int] = Field(title='ID')

    def entity_to_data(self) -> dict:
        data = self.__dict__
        data.pop('id')
        return data


class AggregateRoot(Entity):
    ...
