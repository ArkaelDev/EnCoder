from app.logger import logger
from fastapi import Request

async def log_middleware(request: Request, call_next): #Standard way to create middleware in fastapi
   
    response = await call_next(request)

    log_dict = {
        'url': request.url.path,
        'method': request.method,
        'status_code': response.status_code,
    } 
    logger.info(log_dict)
    return response