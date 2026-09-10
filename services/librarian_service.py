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
        service = librarian_service()

        books = service.view_catalogue()

        assert books == []

    def search_books(self, title):
        return[
            book for book in self.books
            if title.lower() in book.title.lower()
        ]
    