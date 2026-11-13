from fastapi import APIRouter, Request, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from backend.schema.Item_Schema import Item_Schema
from backend.database.db import get_db
from backend.service import file_service, item_service, user_service
from backend.curr_user import get_current_user
from backend.templates import templates


router = APIRouter(prefix="/item", tags=["item"])


@router.get("/lost")
def get_lost_items(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    lost_items = item_service.get_items(db, "Lost")
    user_name = user_service.get_user_details(user_id, db).get("user_name")

    return templates.TemplateResponse(
        request=request,
        name="ItemsPage.html",
        context={"items": lost_items, "page_title": "Reported Lost Items", "user_name": user_name}
    )


@router.post("/lost")
def report_lost_item(
    item_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    image_path = None

    try:
        data = Item_Schema.model_validate_json(item_data)
        image_path = file_service.save_item_image(image)
        item = item_service.register_item(data, "Lost", image_path, user_id, db)

    except ValueError as e:

        file_service.delete_item_image(image_path)
        raise HTTPException(status_code=400, detail=str(e))


    return True
    

@router.get("/found")
def get_found_items(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    found_items = item_service.get_items(db, "Found")
    user_name = user_service.get_user_details(user_id, db).get("user_name")

    return templates.TemplateResponse(
        request=request,
        name="ItemsPage.html",
        context={"items": found_items, "page_title": "Reported Found Items", "user_name": user_name}
    )


@router.post("/found")
def report_found_item(
    item_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    image_path = None

    try:
        data = Item_Schema.model_validate_json(item_data)
        image_path = file_service.save_item_image(image)
        item = item_service.register_item(data, "Found", image_path, user_id, db)

    except ValueError as e:

        file_service.delete_item_image(image_path)
        raise HTTPException(status_code=400, detail=str(e))

    return True


@router.get("/report_form")
def get_report_form(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="ReportForm.html",
        context={}
    )
