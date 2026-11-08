import uuid
from pathlib import Path
from fastapi import UploadFile

upload_dir = Path("backend/uploads/item_images")

def save_item_image(image: UploadFile):

    extention = Path(image.filename).suffix.lower()
    id = uuid.uuid4().hex
    filename = f"{id}{extention}"

    with open(upload_dir / filename, "wb") as f:
        f.write(image.file.read())

    return f"/uploads/item_images/{filename}"

def delete_item_image(image_path: str):

    if image_path:
        path = Path(image_path)

        if path.exists():
            path.unlink()