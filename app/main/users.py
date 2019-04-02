class User():
    def __init__(self, name, room_name, socketId):
        self.user_name = name
        self.room_name = room_name
        self.user_id = socketId
        self.user_score = 0

    def get_user_name(self):
        return self.user_name

    def get_room_name(self):
        return self.room_name

    def get_user_id(self):
        return self.user_id

    def get_user_score(self):
        return self.user_score

    def add_to_user_score(self, score):
        self.user_score = self.user_score + score