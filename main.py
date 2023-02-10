from fastapi import FastAPI

app = FastAPI()

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Checking Reload"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your posts"}