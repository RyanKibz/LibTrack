class Book:
    def __init__(self, title, author, isbn, category):
        if not title:
            raise ValueError(" Book title is required")
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.availability = "Available"