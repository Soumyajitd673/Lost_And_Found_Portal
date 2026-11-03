from pydantic import BaseModel

class Login_Info(BaseModel):

    email: str
    password: str

class Register_Info(BaseModel):

    name: str
    college_id: str
    password: str
    email: str