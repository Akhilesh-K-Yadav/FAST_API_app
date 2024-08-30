# https://www.youtube.com/watch?v=0sOvCWFmrtA

from typing import Union
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from db import engine, session_local, get_db
import models
import schemas
from sqlalchemy.orm import Session
import utils
from routers import posts, users, auth, votes



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='Pa$$w0rd89', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB conn green!!!")
        break
    except Exception as error:
        print("DB conn red")
        print(f"Error:{error}")
        time.sleep(5)



all_posts = [{'title': 'Beaches', 'content': 'Checkout beaches, they are amazing', 'id': 1, 'rating': None},
             {'title': 'Beaches', 'content': 'Checkout beaches, they are amazing', 'id': 2, 'rating': 2},
             {'title': 'Beaches', 'content': 'Checkout beaches, they are amazing', 'id': 3, 'rating': 3}]
 
@app.get("/")
def read_root():
    return {"Hello": "World o yo"}

# @app.get("/posts")
# def get_all_posts():
#     cursor.execute('''SELECT * FROM public."Posts"''')
#     posts = cursor.fetchall()
#     print(posts)
#     return posts

# @app.get("/posts/{id}")
# def get_post(id: int, res: Response): #else the id would be a string by default. Doing this fastapi takes the overhead of i/p validation
#     print(id)
#     if id >= len(all_posts):
#         res.status_code = status.HTTP_404_NOT_FOUND
#         return {"message":f"Post with the id {id} does not exist"}
#     return all_posts[id-1]

#Better way of handling failure scenario
# @app.get("/posts/{id}")
# def get_post(id: int): #else the id would be a string by default. Doing this fastapi takes the overhead of i/p validation
#     print(id)
#     # if id >= len(all_posts):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} does not exist")
#     #     res.status_code = status.HTTP_404_NOT_FOUND
#     #     return {"message":f"Post with the id {id} does not exist"}
    
#     cursor.execute('''SELECT * FROM public."Posts" WHERE id= %s''',str(id))
#     posts = cursor.fetchall()
#     print(posts)
#     return posts
#     #return all_posts[id-1]

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     all_posts.pop(id-1)
#     return


# @router.put("/posts/{id}")
# def update_post(id: int, payload: schemas.Post):
#     if id >= len(all_posts):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} does not exist")
#     all_posts.pop(id-1)
#     all_posts.insert(id-1, payload)
#     return {"msg":"Update success"}

# @app.put("/posts/{id}")
# def update_post(id: int, payload: schemas.Post):
#     cursor.execute(''' INSERT INTO public."Posts" (title, content) VALUES (%s, %s) RETURNING *''', (payload.title, payload.content))
#     ret = cursor.fetchall()
#     print(ret)
#     conn.commit()
#     return {"msg":"Update success"}