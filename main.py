"""
main.py - Entry point for the Library Management System.

Provides a menu-driven command-line interface (CLI) that allows users to:
1. Add Library
2. View All Libraries
3. Add Book
4. View Books in a Library
5. View All Books
6. Search Books
7. Display CSV Data
8. Exit
"""

from library_manager import LibraryManager


def display_menu():
    """Print the main menu options."""
    print("\n" + "=" * 50)
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("  1. Add Library")
    print("  2. View All Libraries")
    print("  3. Add Book")
    print("  4. View Books in a Library")
    print("  5. View All Books")
    print("  6. Search Books")
    print("  7. Display CSV Data")
    print("  8. Exit")
    print("=" * 50)


def add_library(manager):
    """Prompt the user and add a new library."""
    print("\n--- Add New Library ---")
    library_id = input("Enter Library ID: ")
    library_name = input("Enter Library Name: ")
    success, message = manager.add_library(library_id, library_name)
    print(message)


def view_all_libraries(manager):
    """Display all libraries in a formatted table."""
    print("\n--- All Libraries ---")
    libraries = manager.get_all_libraries()
    print(manager.format_library_table(libraries))


def add_book(manager):
    """Prompt the user and add a new book to a library."""
    print("\n--- Add New Book ---")

    # Show existing libraries so the user can pick one
    libraries = manager.get_all_libraries()
    if not libraries:
        print("No libraries exist yet. Please add a library first (option 1).")
        return

    print("Available Libraries:")
    print(manager.format_library_table(libraries))
    print()

    library_id = input("Enter Library ID to add the book to: ")
    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    publication_year = input("Enter Publication Year: ")

    success, message = manager.add_book(
        book_id, title, author, isbn, publication_year, library_id
    )
    print(message)


def view_books_in_library(manager):
    """Display all books belonging to a specific library."""
    print("\n--- View Books in a Library ---")
    libraries = manager.get_all_libraries()
    if not libraries:
        print("No libraries exist yet.")
        return

    print("Available Libraries:")
    print(manager.format_library_table(libraries))
    print()

    library_id = input("Enter Library ID: ")
    if not manager.library_exists(library_id):
        print(f"Error: Library ID '{library_id.strip()}' not found.")
        return

    lib_name = manager.get_library_name(library_id)
    books = manager.get_books_by_library(library_id)
    print(f"\nBooks in '{lib_name}':")
    print(manager.format_book_table(books))


def view_all_books(manager):
    """Display all books across all libraries."""
    print("\n--- All Books ---")
    books = manager.get_all_books()
    print(manager.format_book_table(books))


def search_books(manager):
    """Search for books by title, author, or ISBN."""
    print("\n--- Search Books ---")
    keyword = input("Enter search keyword (title / author / ISBN): ")
    if not keyword.strip():
        print("Error: Search keyword cannot be empty.")
        return

    results = manager.search_books(keyword)
    print(f"\nSearch results for '{keyword.strip()}':")
    print(manager.format_book_table(results))


def display_csv_data(manager):
    """Show raw CSV-style data for both libraries and books."""
    print("\n--- CSV Data: Libraries ---")
    libraries = manager.get_all_libraries()
    if libraries:
        print("  library_id, library_name")
        for lib in libraries:
            print(f"  {lib['library_id']}, {lib['library_name']}")
    else:
        print("  (empty)")

    print("\n--- CSV Data: Books ---")
    books = manager.get_all_books()
    if books:
        print("  book_id, title, author, isbn, publication_year, library_id")
        for book in books:
            print(
                f"  {book['book_id']}, {book['title']}, {book['author']}, "
                f"{book['isbn']}, {book['publication_year']}, {book['library_id']}"
            )
    else:
        print("  (empty)")


def main():
    """Run the Library Management System CLI loop."""
    manager = LibraryManager()
    print("Welcome to the Library Management System!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_library(manager)
        elif choice == "2":
            view_all_libraries(manager)
        elif choice == "3":
            add_book(manager)
        elif choice == "4":
            view_books_in_library(manager)
        elif choice == "5":
            view_all_books(manager)
        elif choice == "6":
            search_books(manager)
        elif choice == "7":
            display_csv_data(manager)
        elif choice == "8":
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
