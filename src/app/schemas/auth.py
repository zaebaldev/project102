from pydantic import BaseModel, EmailStr


class LoginBase(BaseModel):
    password: str


class LoginWithEmail(LoginBase):
    email: EmailStr


class VerifyCode(BaseModel):
    email: EmailStr
    code: str
