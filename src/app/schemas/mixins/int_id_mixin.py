from pydantic import BaseModel


class IntIdMixin(BaseModel):
    id: int
