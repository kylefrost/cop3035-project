class Room():
    def __init__(self, name, password, host):
        self.room_name = name
        self.room_password = password
        self.room_host = host
        self.users = []

    def get_room_name(self):
        return self.room_name

    def get_room_password(self):
        return self.room_password

    def get_room_host(self):
        return self.room_host

    def get_room_users(self):
        return self.users

    def get_room_host(self):
        return self.room_host

    def remove_room_user(self, name):
        self.users = [x for x in self.users if x.get_user_name() != name]

active_rooms = []
