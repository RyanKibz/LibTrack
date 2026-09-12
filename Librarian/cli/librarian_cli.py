from Librarian.services.librarian_service import LibrarianService


def show_menu():
    print("\nLIBRARIAN MENU")
    print("1. Add Book")
    print("2. View Catalogue")
    print("3. Search Book")
    print("4. Update Availability")
    print("5. Update Book Category")
    print("6. Archive Book")
    print("7. Exit")


def main():
    manage = LibrarianService()

    while True:
        show_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            category = input("Enter category: ")

            try:
                book = manage.add_book(
                    title,
                    author,
                    isbn,
                    category
                )

                print(f"{book.title} added successfully.")

            except ValueError as error:
                print(error)

        elif choice == "2":
            books = manage.view_catalogue()

            if not books:
                print("Catalogue is empty.")
            else:
                for book in books:
                    print(
                        f"{book.title} | "
                        f"{book.author} | "
                        f"{book.isbn} | "
                        f"{book.category} | "
                        f"{book.availability}"
                    )

        elif choice == "3":
            search_term = input(
                "Enter title, author or ISBN: "
            )

            results = manage.search_books(search_term)

            if not results:
                print("No books found.")
            else:
                for book in results:
                    print(
                        f"{book.title} | "
                        f"{book.author} | "
                        f"{book.isbn} | "
                        f"{book.availability}"
                    )

        elif choice == "4":
            isbn = input("Enter ISBN: ")
            status = input(
                "Enter status "
                "(Available/Unavailable/Missing/Archived): "
            )

            try:
                book = manage.update_availability(
                    isbn,
                    status
                )

                print(
                    f"{book.title} is now "
                    f"{book.availability}."
                )

            except ValueError as error:
                print(error)

        elif choice == "5":
            isbn = input("Enter ISBN: ")
            category = input("Enter new category: ")

            try:
                book = manage.update_book(
                    isbn,
                    category
                )

                print(
                    f"{book.title} category updated "
                    f"to {book.category}."
                )

            except ValueError as error:
                print(error)

        elif choice == "6":
            isbn = input("Enter ISBN: ")

            try:
                book = manage.archive_book(isbn)

                print(
                    f"{book.title} has been archived."
                )

            except ValueError as error:
                print(error)

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()