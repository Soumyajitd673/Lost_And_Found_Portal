from pydantic import BaseModel

class Item_Schema(BaseModel):

    title: str
    description: str | None = None
    category: str
    location: str
    