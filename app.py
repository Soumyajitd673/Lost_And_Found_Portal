from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import user_routes, item_routes


app = FastAPI()


app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

app.include_router(user_routes.router)

app.include_router(item_routes.router)
