import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import re

from backend.models.user import User
from backend.schema.Login_Register_Info_Schema import Register_Info, Login_Info
from backend.service import email_service



def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@iitbhilai\.ac\.in$'
    return bool(re.match(email_regex, email))


def validate_password(password: str) -> bool:
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(password_regex, password))

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_user(db: Session, data: Register_Info):

    if not validate_email(data.email) or not validate_password(data.password):
        raise ValueError("Bad email or password.")

    if get_user_by_email(db, data.email):
        raise ValueError("Email already registered.")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(str(e))

    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.scalars(select(User).where(User.id == user_id)).first()

def get_user_by_email(db: Session, email: str):
    return db.scalars(select(User).where(User.email == email)).first()


def authenticate_user(db: Session, data: Login_Info):

    user = get_user_by_email(db, data.email)

    if user is None:
        return None

    if not verify_password(data.password, user.password_hash):
        return None

    return user


def is_admin(db: Session, user_id: int):

    user = get_user_by_id(db, user_id)
    return user.role == "admin"


def get_user_details(user_id: int, db: Session):

    user = get_user_by_id(db, user_id)

    details = {
        "user_name": user.name,
        "user_email": user.email,
        "user_role": user.role
    }

    return details

def delete_user(db: Session, user_id: int, input_password: str):

    user = get_user_by_id(db, user_id)

    if not verify_password(input_password, user.password_hash):
        raise ValueError("Incorrect Password")

    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(str(e))
