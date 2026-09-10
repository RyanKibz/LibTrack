import pytest
from models.book import Book


class LibrarianService:
    def __init__(self):
        self.books = []


    def add_book(self, title, author, isbn, category):
        for book in self.books:
            if book.isbn == isbn:
                raise ValueError("A book with this ISBN already exists")
        book = Book(title, author, isbn, category)
        self.books.append(book)
        return book

    def view_catalogue(self):
        return self.books

    def test_empty_catalogue_returns_empty_list():
        service = LibrarianService()

        books = service.view_catalogue()

        assert books == []

    
    def search_books(self, search_term):
        return [
            book for book in self.books
            if search_term.lower() in book.title.lower()
            or search_term.lower() in book.author.lower()
            or search_term.lower() in book.isbn
            ]
    def update_availability(self, isbn, new_status):
        valid_statuses= [
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
                 return book

        raise ValueError("Book not found")