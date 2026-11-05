from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schema.Login_Register_Info_Schema import Login_Info, Register_Info
import backend.service.user_service as user_service
from backend.templates import templates
from backend.database.db import get_db

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/login")
def get_login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
def login(login_info: Login_Info, db: Session = Depends(get_db)):
    
    user = user_service.authenticate_user(db, login_info)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return True


@router.get("/register")
def get_register_page(request: Request):

    return templates.TemplateResponse(
        name="register.html",
        request=request
    )


@router.post("/register")
def register(register_info: Register_Info, db: Session = Depends(get_db)):

    try:
        user = user_service.create_user(db, register_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return True

