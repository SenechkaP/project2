class Post:
    def __init__(self, post_id, author_id, text):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        }
