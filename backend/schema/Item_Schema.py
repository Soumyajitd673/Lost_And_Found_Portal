from pydantic import BaseModel

class Item(BaseModel):

    title: str
    description: str | None = None
    category: str
    location: str | None = None
    