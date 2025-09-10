from datetime import datetime

from pydantic import BaseModel

from src.utils import SetNonesMixin


class PropertyCreateInfo(BaseModel):
    title: str | None
    cost: int | None
    quota: str | None
    location: str | None
    main_photo: str | None
    owner_id: str | None
    type: str | None = None
    description: str | None = None


class PropertyUpdateInfo(PropertyCreateInfo, SetNonesMixin):
    pass


class PropertyInfo(PropertyCreateInfo):
    property_id: str
    created_at: datetime
