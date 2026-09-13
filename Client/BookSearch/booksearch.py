def search_books(query, books):
    
    
    if not query or not query.strip():
        return []

    query_lower = query.strip().lower()
    results = []

    for book in books:
        if (
            query_lower in book["title"].lower()
            or query_lower in book["author"].lower()
            or query_lower == book["isbn"].lower()
        ):
            results.append(book)

    return results