# UserSelection class which keeps track of all the book & ratings the user has selected
class UserSelection:

    user_selections = {}

    def __init__(self):
        self.user_selections = {'The Hunger Games (The Hunger Games, #1)': 1,
                                "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)": 2,
                                'To Kill a Mockingbird': 3,
                                'The Fault in Our Stars': 1, 'The Hobbit': 5}

    def get_user_selection(self) -> dict:
        return self.user_selections

    def set_user_selection(self, book_title: str, book_rating: str):
        self.user_selections[book_title] = int(book_rating)

    def clear_selections(self):
        self.user_selections.clear()

    def get_length(self) -> int:
        return len(self.user_selections)

    def del_selection(self, key: str):
        self.user_selections.pop(key)
