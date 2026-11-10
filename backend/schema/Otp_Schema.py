from pydantic import BaseModel


class Otp_Request(BaseModel):
    email: str


class Otp_Verify(BaseModel):
    email: str
    otp: str
