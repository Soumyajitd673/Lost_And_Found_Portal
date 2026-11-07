from sqlalchemy.orm import Session

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
    