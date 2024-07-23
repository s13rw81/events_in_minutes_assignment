from contextlib import asynccontextmanager

import uvicorn
from api.auth.authentication import auth_api_router
from api.bookings.bookings_api import bookings_api_router
from api.user.user_api import user_api_router
from config import PORT, DEBUG, HOST
from data.db import init_db
from fastapi import FastAPI, Request
from logging_config import log
from starlette.responses import RedirectResponse, JSONResponse


@asynccontextmanager
async def start_db(app):
    await init_db()
    yield


app = FastAPI(lifespan = start_db)
# api routers
app.include_router(auth_api_router)
app.include_router(bookings_api_router)
app.include_router(user_api_router)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code = 400,
        content = {"message": exc.errors()[0]['msg']},
    )


@app.get("/", include_in_schema = False)
async def root(request: Request):
    log.info(f"method: {request.method}, headers: {request.headers}, client: {request.client}")
    return RedirectResponse(url = "/docs")


if __name__ == '__main__':
    uvicorn.run("main:app", host = HOST, port = PORT, reload = DEBUG)
