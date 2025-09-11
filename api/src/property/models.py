from datetime import datetime

from pydantic import BaseModel

from src.utils import SetNonesMixin


class PropertyCreateInfo(BaseModel):
    title: str | None
    cost: int | None
    quota: int | None
    location: str | None
    main_photo: str | None
    type: str | None = None
    description: str | None = None


class PropertyUpdateInfo(PropertyCreateInfo, SetNonesMixin):
    pass


class PropertyInfo(PropertyCreateInfo):
    owner_id: str
    property_id: int
    created_at: datetime

    @staticmethod
    def foreign_key(value: str):
        return {'owner_id': value}

    @staticmethod
    def identify_property(value: int):
        return {'property_id': value}
