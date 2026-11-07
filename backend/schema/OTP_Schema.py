from pydantic import BaseModel


class Send_OTP_Info(BaseModel):
    email: str


class Verify_OTP_Info(BaseModel):
    email: str
    otp: str