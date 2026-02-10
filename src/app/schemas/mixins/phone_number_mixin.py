from typing import Annotated

from pydantic import BaseModel, Field

PHONE_NUMBER_FIELD = Annotated[
    str, Field(pattern=r"^[1-9]\d{1,14}$", examples=["998991234567"])
]

PHONE_NUMBER_FIELD_UPDATE = Annotated[
    str | None,
    Field(
        pattern=r"^[1-9]\d{1,14}$",
        examples=["998991112233"],
        default=None,
    ),
]


class PhoneNumberMixin(BaseModel):
    phone_number: PHONE_NUMBER_FIELD


class PhoneNumberUpdateMixin(BaseModel):
    phone_number: PHONE_NUMBER_FIELD_UPDATE
