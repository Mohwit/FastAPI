from fastapi import FastAPI

from schema.Post import Post

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello!"}


@app.get("/posts")
def get_post():
    return {"Post": 1}


@app.post("/createposts")
def create_post(post: Post):
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)
    ## converting pydantic model to dictionary
    print(post.dict())
    return {
        "new_post": f"Title: {post.title}, content: {post.content}, published: {post.published}, rating: {post.rating}"
    }
