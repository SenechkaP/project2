from flask import Flask

app = Flask(__name__)
USERS = []
POSTS = []

from app import user
from app import post
from app import views
from app import tests
