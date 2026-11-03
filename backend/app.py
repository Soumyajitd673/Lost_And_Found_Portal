from fastapi import FastAPI

from backend.routes import user_routes, item_routes


app = FastAPI()

app.include_router(user_routes.router)

app.include_router(item_routes.router)
