from fastapi import FastAPI, Response, status, HTTPException

from schema.Post import Post
from random import randint

app = FastAPI()

my_posts = [
    {"title": "Title 1", "content": "content 1", "id": 1},
    {"title": "Title 2", "content": "content 2", "id": 2},
]


def retrieve_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def retrieve_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hi"}


@app.get("/posts")
def get_post():
    return {"Post": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def latest_post():
    length = len(my_posts)
    return my_posts[length - 1]


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = retrieve_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_details": retrieve_post(id)}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = retrieve_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exists",
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
