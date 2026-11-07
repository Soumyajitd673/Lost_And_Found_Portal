from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.schema.Login_Register_Info_Schema import Login_Info, Register_Info
from backend.schema.OTP_Schema import Send_OTP_Info, Verify_OTP_Info
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

    if not user_service.is_email_verified(register_info.email):
        return JSONResponse(
            status_code=403,
            content={"error": "Email not verified. Please verify with an OTP."}
        )

    try:
        user_service.create_user(db, register_info)
    except ValueError as e:
        if str(e) == "Email already registered.":
            return JSONResponse(status_code=409, content={"error": "This email is already registered. Please log in."})
        return JSONResponse(status_code=500, content={"error": "Could not register user."})

    user_service.remove_verified_email(register_info.email)
    return {"register": "successful"}


@router.post("/send-otp")
def send_otp(otp_info: Send_OTP_Info, db: Session = Depends(get_db)):
    email = otp_info.email.strip().lower()
    if not user_service.is_valid_college_email(email):
        return JSONResponse(
            status_code=400,
            content={"error": "Use a valid college email ending in @iitbhilai.ac.in"}
        )

    if user_service.get_user_by_email(db, email):
        return JSONResponse(
            status_code=409,
            content={"error": "This email is already registered. Please log in."}
        )

    if not user_service.send_otp(email):
        return JSONResponse(
            status_code=500,
            content={"error": "Could not send the email. Try again later."}
        )

    return {"message": "OTP sent"}


@router.post("/verify-otp")
def verify_otp(otp_info: Verify_OTP_Info):
    result = user_service.verify_otp(otp_info.email, otp_info.otp)
    errors = {
        "missing": (400, "Please send an OTP first."),
        "expired": (400, "OTP expired. Request a new one."),
        "too_many_attempts": (400, "Too many wrong attempts. Request a new OTP."),
        "incorrect": (400, "Incorrect OTP."),
    }
    if result in errors:
        status_code, message = errors[result]
        return JSONResponse(status_code=status_code, content={"error": message})
    return {"message": "Email verified"}

