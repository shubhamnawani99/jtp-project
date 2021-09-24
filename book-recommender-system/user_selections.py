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

    def not_null(self) -> bool:
        return len(self.user_selections) > 0

# self.user_selections = {'The Hunger Games (The Hunger Games, #1)': 1,
#                         "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)": 2,
#                         'To Kill a Mockingbird': 3,
#                         'The Fault in Our Stars': 1, 'The Hobbit': 5}

# self.user_selections = {'Bleach, Volume 01': 5,
#                         'Naruto, Vol. 01: The Tests of the Ninja (Naruto, #1)': 5,
#                         'One Piece, Volume 01: Romance Dawn (One Piece, #1)': 4,
#                         'Fullmetal Alchemist, Vol. 1 (Fullmetal Alchemist, #1)': 4,
#                         'Fruits Basket, Vol. 1': 4}
