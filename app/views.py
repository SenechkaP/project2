from app import app, USERS, POSTS, models
from flask import request, Response, send_file
from http import HTTPStatus
import matplotlib.pyplot as plt
import matplotlib
import json

matplotlib.use("Agg")


@app.route("/")
def index():
    return "<h1> Hello <h1>"


@app.post("/users/create")
def create_user():
    data = request.json
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(first_name, last_name, email, user_id)
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
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.uid,
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


@app.post("/posts/create")
def create_post():
    data = request.json
    post_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]

    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = models.Post(post_id, author_id, text)
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


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id):
    if user_id < 0 or user_id >= len(USERS):
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
        json.dumps({"posts": [post.convert_to_dict() for post in user_sorted_posts]}),
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
                {"users": [user.convert_to_dict() for user in users_leaderboard]}
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif data["type"] == "graph":
        x = [user.user_id for user in USERS]
        y = [user.total_reactions for user in USERS]
        plt.plot(x, y)
        plt.savefig("app/graph.png")
        return send_file("graph.png", mimetype="image/gif")
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
