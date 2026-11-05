from pydantic import BaseModel

class Login_Info(BaseModel):

    email: str
    role: str
    password: str

class Register_Info(BaseModel):

    name: str
    role: str
    password: str
    email: str