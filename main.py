from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

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

my_posts = [{'title' : 'title of post 1', "content" : "content of post 1", "id" : 1}, {"title" : "favorite foods", "content" : "pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Checking Reload"}

@app.get("/posts")
def get_posts():
    # auto conversion to json
    return {"data" : my_posts}

'''#post method for storing data from post request
@app.post("/posts")
#automatically extracts all info from body and stores in a dictionary with name "payload"
def create_posts(payload: dict = Body(...)):
    #prints the payload on the terminal
    print(payload)
    return {"new_post" : f"title : {payload['title']}, content : {payload['content']}"}'''

#accepting post data of the format {title str, content str} enforced using pydantic
@app.post("/posts")
#we reference the post class to give the format that we need the post request body to send
def create_posts(post : Post):
    '''print(post)
    print(post.title)
    print(post.published)
    print(post.rating)
    # to convert pydantic model to dictionary
    print(post.dict())'''

    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

#id field is a path parameter
@app.get("/posts/{id}")
#we need to validate if this is an integer and then convert else throw automatic error
def get_post(id : int):
    #we typecast as int as post request sends the id as a string
    post = find_post(id)
    return {"post detail" : post}
