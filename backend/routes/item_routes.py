from fastapi import APIRouter, Request, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from backend.schema.Item_Schema import Item_Schema
from backend.database.db import get_db
from backend.service import file_service, item_service
from backend.curr_user import get_current_user


router = APIRouter(prefix="/item", tags=["item"])


@router.get("/lost")
def get_lost_items(request: Request):

    return {"html_page": "success", "data": "success"}

@router.post("/lost")
def report_lost_item(
    item_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    image_path = None

    try:
        data = Item_Schema.model_dump_json(item_data)
        image_path = file_service.save_item_image(image)
        item = item_service.register_item(data, "Lost", image_path, user_id, db)

    except ValueError as e:

        file_service.delete_item_image(image_path)
        raise HTTPException(status_code=400, detail=str(e))


    return True
    

@router.get("/found")
def get_lost_items(request: Request):

    return {"html_page": "success", "data": "success"}

@router.post("/found")
def report_found_item(
    item_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    image_path = None

    try:
        data = Item_Schema.model_dump_json(item_data)
        image_path = file_service.save_item_image(image)
        item = item_service.register_item(data, "Found", image_path, user_id, db)

    except ValueError as e:

        file_service.delete_item_image(image_path)
        raise HTTPException(status_code=400, detail=str(e))

    return True


