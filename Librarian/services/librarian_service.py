import json
from models.book import Book



class LibrarianService:
    def __init__(self, data_file="Librarian/data/books.json"):
        self.books = []
        self.data_file = data_file
        self.load_books()

    def load_books(self):
        try:
           with open(self.data_file, "r") as file:
                data = json.load(file)

                self.books = []

                for item in data:
                    book = Book(
                        item["title"],
                        item["author"],
                        item["isbn"],
                        item["category"]
                    )

                    book.availability = item["availability"]
                    self.books.append(book)

        except FileNotFoundError:
            self.books = []

    def save_books(self):
        data = [
            book.to_dict()
            for book in self.books
        ]

        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def add_book(self, title, author, isbn, category):
        for book in self.books:
            if book.isbn == isbn:
                raise ValueError("A book with this ISBN already exists")

        book = Book(title, author, isbn, category)
        self.books.append(book)

        self.save_books()

        return book

    def view_catalogue(self):
        return self.books

    def search_books(self, search_term):
        return [
            book for book in self.books
            if search_term.lower() in book.title.lower()
            or search_term.lower() in book.author.lower()
            or search_term in book.isbn
        ]

    def update_availability(self, isbn, new_status):
        valid_statuses = [
            "Available",
            "Unavailable",
            "Missing",
            "Archived"
        ]

        if new_status not in valid_statuses:
            raise ValueError("Invalid availability status")

        for book in self.books:
            if book.isbn == isbn:
                book.availability = new_status
                self.save_books()
                return book

        raise ValueError("Book not found")

    def update_book(self, isbn, new_category):
        for book in self.books:
            if book.isbn == isbn:
                book.category = new_category
                self.save_books()
                return book

        raise ValueError("Book not found")

    def archive_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.availability = "Archived"
                self.save_books()
                return book

        raise ValueError("Book not found")