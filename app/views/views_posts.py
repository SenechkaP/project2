from app import app, USERS, POSTS
from app.post import Post
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/posts/create")
def create_post():
    data = request.json
    post_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]

    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = Post(post_id, author_id, text)
    USERS[author_id].posts.append(post)
    POSTS.append(post)
    response = Response(
        json.dumps(
            {
                "id": post.post_id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.post_id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def post_reaction(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    data = request.json
    user_id = data["user_id"]
    reaction = data["reaction"]

    USERS[user_id].total_reactions += 1
    POSTS[post_id].reactions.append(reaction)

    return Response(status=HTTPStatus.OK)
