from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db
# from . import models
# from .database import engine

# this is going to create the model in the main file
models.Base.metadata.create_all(bind = engine)

'''
This code is for when you directly want to connect with a SQL table using psycopg
'''
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '1998', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error - ", error)
        time.sleep(2)

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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/sqlalchemy")
# we basically create a session as soon as the url gets hit
def test_posts(db : Session = Depends(get_db)):
    # this returns all the posts in the database
    posts = db.query(models.Post).all()
    return {"Data" : posts}

#This is called a route or path operation
@app.get("/")
async def root():
    return {"message": "Welcome to the API practice application using FastAPI"}

@app.get("/posts")
def get_posts():
    # auto conversion to json
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data' : posts}

#accepting post data of the format {title str, content str} enforced using pydantic
@app.post("/posts", status_code=status.HTTP_201_CREATED)
#we reference the post class to give the format that we need the post request body to send
def create_posts(post : Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # need to commit to finalize the input in the database
    conn.commit()
    return {"data" : new_post}

#we put this above the /posts/{id} since fast api validates URL on the basis of order, it will try to insert "latest" as an int int the below function and throw an error
#to avoid this, we make sure it finds /posts/latest/ first and then the id one
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail" : post}


#id field is a path parameter
@app.get("/posts/{id}")
#we need to validate if this is an integer and then convert else throw automatic error and take response object for this function
def get_post(id : int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    #send an error code if not found and throw an error
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {'deleted post' : deleted_post}

@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return {'data' : updated_post}