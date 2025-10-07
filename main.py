from fastapi import FastAPI, status

app = FastAPI()


@app.get("/")
async def root(status_code=status.HTTP_200_OK):
    '''Default route, only use is to know if the server is running'''
    return {"message": "Service is running, please log in"}