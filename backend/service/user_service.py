import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.schema.Login_Register_Info_Schema import Register_Info, Login_Info

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_user(db: Session, data: Register_Info):

    if get_user_by_email(db, data.email):
        raise ValueError("Email already registered.")

    user = User(
        name=data.name,
        role="user",
        email=data.email,
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

    if user is None:
        return None

    if not verify_password(data.password, user.password_hash):
        return None

    return user