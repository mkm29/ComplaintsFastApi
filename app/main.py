from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import settings
from .db import database
from .resources.routes import api_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    openapi_url="/openapi.json",
)
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
