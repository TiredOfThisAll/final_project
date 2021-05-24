class User:
    def __init__(self, id, name, email, picture):
        self.id = id
        self.name = name
        self.email = email
        self.picture = picture

    def from_tuple(user_tuple):
        return User(*user_tuple)

    def __str__(self):
        return "User: " \
            + f"id = {self.id}, " \
            + f"name = {self.name}, " \
            + f"email = {self.email}, " \
            + f"picture = {self.picture}, " \

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
