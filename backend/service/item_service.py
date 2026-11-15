from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from backend.models.item import Item
from backend.models.category import Category
from backend.schema.Item_Schema import Item_Schema


def get_category_id(db: Session, category: str):

    category_id = db.scalar(select(Category.id).where(Category.name == category))

    return category_id

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
        category_id=get_category_id(db, data.category),
        status="Active",
        location=data.location,
        image_url=image_path,
        reported_by=user_id,
    )

    db.add(item)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(str(e))

    db.refresh(item)

    return item


def get_item_by_id(db: Session, item_id: int):

    return db.scalar(select(Item).where(Item.id == item_id))

def get_items(db: Session, report_type: str):

    return db.scalars(select(Item).where(Item.report == report_type)).all()

def get_items_by_category(db: Session, category: str, report_type: str):

    return db.scalars(
        select(Item)
        .join(Item.category)
        .where(Item.report == report_type, Category.name == category)
    ).all()

def get_items_count(db: Session, report_type: str):

    return db.scalar(select(func.count()).select_from(Item).where(Item.report == report_type))

def get_user_reported_items(db: Session, user_id: int):

    items = db.scalars(select(Item).where(Item.reported_by == user_id)).all()

    result = {
        "lostItems": [],
        "foundItems": []
    }

    for item in items:

        data = {
            "item_id": item.id,
            "item_name": item.title,
            "date_reported": item.created_at,
            "status": item.status
        }

        if item.report == "Lost":
            result["lostItems"].append(data)
        else:
            result["foundItems"].append(data)

    return result

def mark_as_returned(db: Session, item_id: int, user_id: int):

    item = get_item_by_id(db, item_id)

    if not item or item.reported_by != user_id:
        raise ValueError()

    item.status = "Returned"

    db.commit()
    db.refresh(item)

    return item


def delete_item(db: Session, item_id: int, user_id: int):

    item = get_item_by_id(db, item_id)

    if not item or item.reported_by != user_id:
        raise ValueError()

    db.delete(item)
    db.commit()

    return item
