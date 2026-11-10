from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.service import user_service
from backend.database.db import get_db

router = APIRouter(prefix="/report", tags=["report"])

@router.get()
def get_reports_page(request: Request, db: Session = Depends(get_db)):

    user_id = Session.get("user_id")

    if user_service.is_admin(db, user_id):
        return True
    else:
        raise HTTPException(status_code=400, detail="Only Admin Access.")


@router.post()
def create_report():

    pass
