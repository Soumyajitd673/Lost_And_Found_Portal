import os
import re
import secrets
import smtplib
import bcrypt
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.schema.Login_Register_Info_Schema import Register_Info, Login_Info

pending_otps = {}
verified_emails = {}


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_user(db: Session, data: Register_Info):

    email = data.email.strip()
    if get_user_by_email(db, email):
        raise ValueError("Email already registered.")

    user = User(
        name=data.name,
        role=data.role,
        email=email,
        password_hash=hash_password(data.password)
    )

    db.add(user)

    try:
        db.commit()
    except:
        db.rollback()
        raise ValueError("Error from database.")

    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.scalars(select(User).where(User.id == user_id)).first()

def get_user_by_email(db: Session, email: str):
    return db.scalars(select(User).where(User.email == email)).first()


def authenticate_user(db: Session, data: Login_Info):

    user = get_user_by_email(db, data.email)

    if user is None or user.role != data.role:
        return None

    if not verify_password(data.password, user.password_hash):
        return None

    return user


def is_valid_college_email(email: str):
    return re.fullmatch(r"[^@\s]+@iitbhilai\.ac\.in", email.strip(), re.IGNORECASE) is not None


def send_otp(email: str):
    email_key = email.strip().lower()
    otp = f"{secrets.randbelow(1000000):06d}"
    pending_otps[email_key] = {
        "otp": otp,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5),
        "attempts": 0,
    }
    verified_emails.pop(email_key, None)

    smtp_host = os.getenv("SMTP_HOST")
    if not smtp_host:
        print(f"OTP for {email_key}: {otp}")
        return True

    try:
        message = EmailMessage()
        message["Subject"] = "Campus Lost and Found Portal email verification"
        message["From"] = os.getenv("SMTP_USER") or "no-reply@iitbhilai.ac.in"
        message["To"] = email_key
        message.set_content(f"Your verification code is {otp}. It expires in 5 minutes.")

        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as smtp:
            smtp.starttls()
            smtp_user = os.getenv("SMTP_USER")
            smtp_pass = os.getenv("SMTP_PASS")
            if smtp_user and smtp_pass:
                smtp.login(smtp_user, smtp_pass)
            smtp.send_message(message)
        return True
    except Exception:
        pending_otps.pop(email_key, None)
        return False


def verify_otp(email: str, otp: str):
    email_key = email.strip().lower()
    otp_data = pending_otps.get(email_key)

    if otp_data is None:
        return "missing"
    if otp_data["expires_at"] <= datetime.now(timezone.utc):
        pending_otps.pop(email_key, None)
        return "expired"
    if otp_data["attempts"] >= 5:
        pending_otps.pop(email_key, None)
        return "too_many_attempts"
    if otp_data["otp"] != otp:
        otp_data["attempts"] += 1
        return "incorrect"

    pending_otps.pop(email_key, None)
    verified_emails[email_key] = datetime.now(timezone.utc) + timedelta(minutes=15)
    return "verified"


def is_email_verified(email: str):
    email_key = email.strip().lower()
    expires_at = verified_emails.get(email_key)
    if expires_at is None:
        return False
    if expires_at <= datetime.now(timezone.utc):
        verified_emails.pop(email_key, None)
        return False
    return True


def remove_verified_email(email: str):
    verified_emails.pop(email.strip().lower(), None)