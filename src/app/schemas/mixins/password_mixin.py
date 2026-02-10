from pydantic import BaseModel


class PasswordMixin(BaseModel):
    password: str  # TODO: with Field from pydantic we can add min and max length
