from models.book import Book

class librarian_service:
    def __init__(self):
        self.books = []


    def add_book(self, title, author, isbn, category):
        book = Book(title, author, isbn, category)
        self.books.append(book)
        return book

    