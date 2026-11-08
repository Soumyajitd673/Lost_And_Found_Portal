from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import func

from backend.models.item import Item
from backend.schema.Item_Schema import Item_Schema



def register_item(
        data: Item_Schema, 
        report: str, 
        image_path: str,
        user_id: int,
        db: Session
):

    item = Item(
        report=report,
        title=data.title,
        description=data.description,
        category=data.category,
        status="Active",
        location=data.location,
        image_url=image_path,
        reported_by=user_id,
    )

    db.add(item)

    try:
        db.commit()
    except:
        db.rollback()
        raise ValueError("Error from database")

    db.refresh()
    return item


def get_items(db: Session, report_type: str):

    return db.scalars(select(Item).where(Item.report == report_type)).all()

def get_items_by_category(db: Session, category: str, report_type: str):

    return db.scalars(select(Item).where(Item.report == report_type, Item.category == category)).all()

def get_items_count(db: Session, report_type: str):

    return db.scalar(select(func.count()).select_from(Item).where(Item.report == report_type))