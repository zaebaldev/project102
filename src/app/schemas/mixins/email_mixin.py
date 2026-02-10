from typing import Optional

from pydantic import BaseModel, EmailStr


class EmailMixin(BaseModel):
    email: EmailStr


class EmailUpdateMixin(BaseModel):
    email: Optional[EmailStr] = None
