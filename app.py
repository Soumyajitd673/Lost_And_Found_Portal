from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from backend.routes import user_routes, item_routes

from backend.database.db import Base, engine
from backend.models import user  # add "item" here only if backend/models/item.py exists

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

app.include_router(user_routes.router)

app.include_router(item_routes.router)




@app.get("/")
def default(request: Request):
    return user_routes.get_login_page(request)
