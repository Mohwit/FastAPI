import time

from fastapi import FastAPI, Response, status, HTTPException
import psycopg

from typing import Dict

from schema.Post import Post

app = FastAPI()

while True:
    try:
        conn = psycopg.connect(
            "host= localhost dbname= fastapi user=postgres password=postgres"
        )

        cursor = conn.cursor()
        print("Connected to database!!")
        break

    except Exception as e:
        print("Failed to connect with database!!")
        print(f"Error: {e}")
        print("Waiting....")
        time.sleep(2)


@app.get("/")
def root() -> Dict:
    return {"message": "Welcome to FastAPI"}


@app.get("/posts")
def get_posts() -> Dict:
    cursor.execute(
        """
    SELECT * from posts;
    """
    )
    products = cursor.fetchall()
    return {"data": products}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post) -> Dict:
    cursor.execute(
        """
    INSERT INTO posts(title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *
    """,
        (new_post.title, new_post.content, new_post.published, new_post.rating),
    )

    post = cursor.fetchone()
    conn.commit()

    return {"data": post}


@app.get("/posts/{pid}")
def get_post(pid: int) -> Dict:
    cursor.execute(
        """
            SELECT * FROM posts WHERE Id = %s
            """,
        (pid,),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {pid} not found",
        )
    return {"Post": post}


@app.delete("/posts/{pid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pid: int) -> Response:

    cursor.execute(
        """
    DELETE FROM posts WHERE Id = (%s) returning *
    """,
        (pid,),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{pid} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{pid}")
def update_post(pid: int, updated_post: Post) -> Dict:
    cursor.execute(
        """
    UPDATE posts SET title = %s, content = %s, published = %s WHERE Id = %s RETURNING *
    """,
        (updated_post.title, updated_post.content, updated_post.published, pid),
    )

    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {pid} not found",
        )

    return {"Updated Post": post}
