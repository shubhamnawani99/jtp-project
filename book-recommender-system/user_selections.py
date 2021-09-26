class UserSelection:
    """UserSelection class which keeps track of all the books & ratings the user has selected"""
    user_selections = {}

    def __init__(self):
        """Define a user selection for testing purposes"""
        self.user_selections = {}

    def get_user_selection(self) -> dict:
        """

        :return: Returns the user selections - books titles and ratings
        """
        return self.user_selections

    def set_user_selection(self, book_title: str, book_rating: str):
        """Sets the book title and book ratings given by the user

        :param book_title: book title selected by the user
        :param book_rating: book ratings given by the user (1-5)
        :return: None
        """
        self.user_selections[book_title] = int(book_rating)

    def clear_selections(self):
        """Clear all the user selections, deletes both book title and ratings

        :return: None
        """
        self.user_selections.clear()

    def get_length(self) -> int:
        """Get the amount of selections made by the user

        :return: The number of books the user has selected
        """
        return len(self.user_selections)

    def del_selection(self, key: str):
        """Deletes a particular selected book from the existing selections

        :param key: the book title to be deleted
        :return: None
        """
        self.user_selections.pop(key)

    def not_null(self) -> bool:
        """

        :return: Whether the current list is empty or not
        """
        return len(self.user_selections) > 0
