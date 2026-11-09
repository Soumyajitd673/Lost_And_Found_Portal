from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import user_routes, item_routes

from backend.database.db import Base, engine
from backend.models.user import User
from backend.models.item import Item
from backend.models.category import Category

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

app.include_router(user_routes.router)
app.include_router(item_routes.router)


@app.get("/")
def default(request: Request):
    return user_routes.get_login_page(request)
