class Book:
    def __init__(
        self,
        title,
        author,
        isbn,
        category,
        branch_id
    ):
        if not title:
            raise ValueError("Book title is required")

        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.branch_id = branch_id
        self.availability = "Available"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "category": self.category,
            "branch_id": self.branch_id,
            "availability": self.availability
        }