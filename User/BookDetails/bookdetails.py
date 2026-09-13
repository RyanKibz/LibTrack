def get_book_details(book_id, books):
    
    
    for book in books:
        if book["id"] == book_id:
            return book
    return None