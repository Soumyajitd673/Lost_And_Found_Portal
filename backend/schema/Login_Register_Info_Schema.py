from typing import Literal
from pydantic import BaseModel, Field

class Login_Info(BaseModel):

    email: str
    role: str
    password: str

class Register_Info(BaseModel):

    name: str
    role: Literal["student", "faculty"]
    password: str = Field(alias="pass")
    email: str
