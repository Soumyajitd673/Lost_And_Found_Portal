from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.schema.Otp_Schema import Otp_Request, Otp_Verify
from backend.service import email_service, otp_service, user_service


router = APIRouter(prefix="/otp", tags=["otp"])


@router.post("/request")
def request_otp(otp_request: Otp_Request, db: Session = Depends(get_db)):
    email = otp_request.email.strip().lower()

    if user_service.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="This email is already registered.")

    try:
        otp = otp_service.create_otp(email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        email_service.send_otp_email(email, otp)
    except Exception:
        otp_service.remove_otp(email)
        raise HTTPException(status_code=500, detail="Could not send OTP email.")

    return {"message": "OTP sent."}


@router.post("/verify")
def verify_email(otp_info: Otp_Verify):
    if not otp_service.verify_otp(otp_info.email, otp_info.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    return {"message": "Email verified."}
