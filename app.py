from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.routes import user_routes, item_routes, otp_routes, report_routes
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

from backend.database.db import Base, engine
from backend.models.user import User
from backend.models.item import Item
from backend.models.category import Category
from backend.models import user, item, category
from backend.database.setup_categories import setup_categories

from backend.curr_user import NotAuthenticated

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)
setup_categories()

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
app.include_router(otp_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def default(request: Request):
    return user_routes.get_login_page(request)


@app.exception_handler(NotAuthenticated)
async def not_authenticated_handler(request: Request, exc: NotAuthenticated):
    return RedirectResponse(url="/", status_code=303)