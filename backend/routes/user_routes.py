from fastapi import APIRouter, Request

from backend.schema.Login_Register_Info_Schema import Login_Info, Register_Info

router = APIRouter(prefix="/user", tags=["user"])




@router.get("/login")
def get_login_page(request: Request):

    return {"login_page": "success"}


@router.post("/login")
def login(login_info: Login_Info):
    
    return {"login": "successful"}


@router.get("/register")
def get_register_page(request: Request):

    return {"register_page": "success"}


@router.post("/register")
def register(register_info: Register_Info):

    return {"register": "successful"}

