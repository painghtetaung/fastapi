from random import randrange
from typing import Optional, Union

from fastapi import Body, FastAPI, Response, status, HTTPException

from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:  str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1"}, {"id": 2, "title": "favorite foods", "content": "I like pizza"}]

def find_post(id):
    for post in my_posts:
        if(post["id"] == id):
            return post

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post, "type of post")
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": "Post not found"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}