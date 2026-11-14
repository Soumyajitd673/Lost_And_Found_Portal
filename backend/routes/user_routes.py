from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schema.Login_Register_Info_Schema import Login_Info, Register_Info
from backend.schema.Delete_Account_Request import DeleteAccountRequest
from backend.service import user_service, otp_service, item_service
from backend.templates import templates
from backend.database.db import get_db
from backend.curr_user import get_current_user


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

    request.session["user_id"] = user.id

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

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return get_login_page(request)


@router.get("/dashboard")
def get_user_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
    ):

    user_name = user_service.get_user_details(user_id, db).get("user_name")

    return templates.TemplateResponse(
        request=request,
        name="Dashboard.html",
        context={"user_name": user_name}
    )

@router.get("/profile")
def get_user_profile(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
    ):

    user_details = user_service.get_user_details(user_id, db)

    return templates.TemplateResponse(
        request=request,
        name='profile.html',
        context=user_details
    )

@router.get("/history")
def get_user_history(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
    ):

    user_history = item_service.get_user_reported_items(db, user_id)

    return user_history


@router.delete("/delete")
def delete_account(
    request: Request,
    delete_request: DeleteAccountRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    try:
        user_service.delete_user(db, user_id, delete_request.password)
        request.session.clear()
        return {"message": "Account deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))