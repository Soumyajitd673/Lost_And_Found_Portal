from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

from backend.routes import user_routes, item_routes
from backend.database.db import Base, engine
from backend.models import user, item, category


Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_KEY"),
    max_age=3600
)


app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")

app.include_router(user_routes.router)

app.include_router(item_routes.router)




@app.get("/")
def default(request: Request):
    return user_routes.get_login_page(request)
