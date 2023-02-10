from fastapi import FastAPI

app = FastAPI()

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Hello World"}
