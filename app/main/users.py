class User():
    def __init__(self, name, room_name, socketId):
        self.user_name = name
        self.room_name = room_name
        self.user_id = socketId
        self.user_score = 0
        self.word_list = []
        self.filtered_list = []
        self.round_score = 0 # Created round_score to be added to overall score then 0ed again

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

    def get_word_list(self):
        return self.word_list

    def add_word_to_list(self, new_word):
        self.word_list.append(new_word)

<<<<<<< HEAD
    def add_filtered_list(self, filtered):
        self.filtered_list = filtered
=======
    def add_filtered_list(self, filtered_list):
        self.filtered_list = filtered_list
>>>>>>> 42a05baa42fd5b7f82f63ed178610f6cc1d09c07
