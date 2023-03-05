from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Monster@0255', cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection to database failed")
    print("Error - ", error)

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
    # rating: Optional[int] = None

my_posts = [{'title' : 'title of post 1', "content" : "content of post 1", "id" : 1}, {"title" : "favorite foods", "content" : "pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Welcome to the API practice application using FastAPI"}

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
@app.post("/posts", status_code=status.HTTP_201_CREATED)
#we reference the post class to give the format that we need the post request body to send
def create_posts(post : Post, response : Response):
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

#we put this above the /posts/{id} since fast api validates URL on the basis of order, it will try to insert "latest" as an int int the below function and throw an error
#to avoid this, we make sure it finds /posts/latest/ first and then the id one
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail" : post}


#id field is a path parameter
@app.get("/posts/{id}")
#we need to validate if this is an integer and then convert else throw automatic error and take response object for this function
def get_post(id : int, response: Response):
    post = find_post(id)
    #send an error code if not found and throw an error
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{' error message' : f"post with id: {id} was not found"}
    return {"post detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post_index = find_index_post(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id : int, post : Post, response : Response):
    post_index = find_index_post(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {'data' : post_dict}