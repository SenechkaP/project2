from app import app, USERS
from app.user import User
from flask import request, Response, send_file
from http import HTTPStatus
import matplotlib.pyplot as plt
import matplotlib
import json

matplotlib.use("Agg")


@app.post("/users/create")
def create_user():
    data = request.json
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = User(first_name, last_name, email, user_id)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not User.is_valid_user(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    if not User.is_valid_user(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    USERS[user_id].status = "deleted"
    response = Response(
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
                "status": "deleted",
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id):
    if not User.is_valid_user(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user_posts = USERS[user_id].posts
    data = request.json

    if data["sort"] == "asc":
        user_sorted_posts = sorted(user_posts, key=lambda post: len(post.reactions))
    elif data["sort"] == "desc":
        user_sorted_posts = sorted(
            user_posts, key=lambda post: len(post.reactions), reverse=True
        )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    response = Response(
        json.dumps({"posts": [post.to_dict() for post in user_sorted_posts]}),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_leaderboard():
    data = request.json
    if data["type"] == "list":
        if data["sort"] == "asc":
            users_leaderboard = sorted(USERS, key=lambda user: user.total_reactions)
        elif data["sort"] == "desc":
            users_leaderboard = sorted(
                USERS, key=lambda user: user.total_reactions, reverse=True
            )
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

        response = Response(
            json.dumps(
                {
                    "users": [
                        user.to_dict()
                        for user in users_leaderboard
                        if User.is_valid_user(user.user_id)
                    ]
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif data["type"] == "graph":
        x = [f"{user.first_name}\n{user.last_name}" for user in USERS]
        y = [user.total_reactions for user in USERS]
        plt.bar(x, y)
        plt.title("Leaderboard")
        plt.ylabel("reactions")
        plt.savefig("app/graph.png")
        return send_file("graph.png")
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
