from fastapi import FastAPI, status
from app.database import engine, Base
from app.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import files

app = FastAPI()
app.include_router(files.router)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware) 
'''We separate that logic from the main app. Using BaseHTTPMiddleware class and overriding dispatch fuction.
We use middleware so every request to our API is passed throught logs.'''
#Base.metadata.create_all(bind=engine)
#This creates tables on the sqldatabase. Be sure to comment before testing

@app.get("/")
async def root(status_code=status.HTTP_200_OK):
    #Only use is to ping
    return {"message": "Service is running, please log in"}

