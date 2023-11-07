from app import app, USERS, POSTS
from app.post import Post
from app.user import User
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/posts/create")
def create_post():
    data = request.json
    post_id = len(POSTS)
    author_id = int(data["author_id"])
    text = data["text"]

    if not User.is_valid_user(author_id):
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
    if not Post.is_valid_post(post_id):
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


@app.delete("/posts/<int:post_id>")
def delete_post(post_id):
    if not Post.is_valid_post(post_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = POSTS[post_id]
    POSTS[post_id].status = "deleted"
    response = Response(
        json.dumps(
            {
                "id": post.post_id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
                "status": "deleted",
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def post_reaction(post_id):
    if not Post.is_valid_post(post_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    data = request.json
    user_id = int(data["user_id"])
    reaction = data["reaction"]

    if not User.is_valid_user(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    USERS[user_id].total_reactions += 1
    POSTS[post_id].reactions.append(reaction)

    return Response(status=HTTPStatus.OK)
