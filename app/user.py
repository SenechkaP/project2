import re
from app import USERS


class User:
    def __init__(self, first_name, last_name, email, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = user_id
        self.total_reactions = 0
        self.posts = []
        self.status = "created"

    @staticmethod
    def is_valid_email(email):
        email_validate_pattern = r"^\S+@\S+\.\S+$"
        return re.match(email_validate_pattern, email)

    @staticmethod
    def is_valid_user(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
        }
