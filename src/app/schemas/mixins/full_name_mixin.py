from typing import Optional

from pydantic import BaseModel


class FullNameMixin(BaseModel):
    full_name: str  # with Field from pydantic we can add mi and max length


class FullNameUpdateMixin(BaseModel):
    full_name: Optional[str] = None
