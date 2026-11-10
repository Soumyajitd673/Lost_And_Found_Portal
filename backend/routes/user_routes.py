from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schema.Login_Register_Info_Schema import Login_Info, Register_Info
import backend.service.user_service as user_service
from backend.templates import templates
from backend.database.db import get_db

from backend.service import otp_service

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/login")
def get_login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
def login(
        login_info: Login_Info,
        request: Request,
        db: Session = Depends(get_db)
    ):
    
    user = user_service.authenticate_user(db, login_info)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    request.session["user.id"] = user.id

    return True


@router.get("/register")
def get_register_page(request: Request):

    return templates.TemplateResponse(
        name="register.html",
        request=request
    )


@router.post("/register")
def register(
    register_info: Register_Info,
    request: Request,
    db: Session = Depends(get_db)
):

    # Check if the email is verified
    if not otp_service.is_email_verified(register_info.email):
        raise HTTPException(status_code=400, detail="Verify your email before registering.")

    try:
        user = user_service.create_user(db, register_info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    otp_service.clear_verified_email(register_info.email)
    request.session["user_id"] = user.id

    return True

@router.post("/logout")
def logout(request: Request):

    request.session["user_id"] = None

    return True
