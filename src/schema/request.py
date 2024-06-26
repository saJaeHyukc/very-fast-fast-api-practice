from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    contents: str
    is_done: bool


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str


class CreateOTPRquest(BaseModel):
    email: str


class VerifyOTPRquest(BaseModel):
    email: str
    otp: int
