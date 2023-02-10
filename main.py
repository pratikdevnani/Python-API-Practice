from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Checking Reload"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your posts"}

#post method for storing data from post request
@app.post("/createposts")
#automatically extracts all info from body and stores in a dictionary with name "payload"
def create_posts(payload: dict = Body(...)):
    #prints the payload on the terminal
    print(payload)
    return {"new_post" : f"title : {payload['title']}, content : {payload['content']}"}