from fastapi import FastAPI, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import Base, engine
from app.middleware import log_middleware
from app.routers import auth, files, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(users.router)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
"""We separate that logic from the main app. Using BaseHTTPMiddleware class and overriding dispatch fuction.
We use middleware so every request to our API is passed throught logs."""
Base.metadata.create_all(bind=engine)
# This creates tables on the sqldatabase. Be sure to comment before testing


@app.get("/")
async def root(status_code=status.HTTP_200_OK):
    # Only use is to ping
    return {"message": "Service is running, please log in"}
