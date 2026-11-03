from fastapi import APIRouter, Request, UploadFile, File, Form
from backend.schema.Item_Schema import Item
from typing import Optional


router = APIRouter(prefix="/item", tags=["item"])


@router.get("/lost")
def get_lost_items(request: Request):

    return {"html_page": "success", "data": "success"}

@router.post("/lost")
def report_lost_item(item_data: str = Form(...), image: Optional[UploadFile] = File(None)):

    return {"lost_report" : "success"}

@router.get("/found")
def get_lost_items(request: Request):

    return {"html_page": "success", "data": "success"}

@router.post("/found")
def report_lost_item(item_data: str = Form(...), image: Optional[UploadFile] = File(None)):

    return {"found_report" : "success"}


