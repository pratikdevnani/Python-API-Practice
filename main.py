from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

'''
Tip: FastAPI matches the first request path with the functions and returns.
So if there are 2 or more methods with the same path route, the first one is the one that will always be sent as response.
'''

#Defining structure for post payload using pydantic
class Post(BaseModel):
    title : str
    content : str
    #can supply default value
    published : bool = True
    #optional field where if the user does not provide, defaults to None
    rating: Optional[int] = None

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

#accepting post data of the format {title str, content str} enforced using pydantic
@app.post("/createPostsCheck")
# we reference the post class to give the format that we need the post request body to send
def create_posts(post : Post):
    print(post)
    print(post.title)
    print(post.published)
    print(post.rating)
    # to convert pydantic model to dictionary
    print(post.dict())
    return {"data" : "new post recieved"}