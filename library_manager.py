"""
library_manager.py - Business logic for the Library Management System.

This module contains the LibraryManager class which handles:
- Creating and listing libraries
- Adding, viewing, and searching books
- Input validation and duplicate checking
"""

import csv_storage


class LibraryManager:
    """Manages libraries and books with CSV-based persistent storage."""

    def __init__(self):
        """Load existing data from CSV files on startup."""
        self.libraries = csv_storage.load_libraries()
        self.books = csv_storage.load_books()

    # ------------------------------------------------------------------
    # Library operations
    # ------------------------------------------------------------------
    def add_library(self, library_id, library_name):
        """
        Add a new library after validating inputs.

        Args:
            library_id (str): Unique identifier for the library.
            library_name (str): Name of the library.

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate inputs
        library_id = library_id.strip()
        library_name = library_name.strip()

        if not library_id:
            return False, "Error: Library ID cannot be empty."
        if not library_name:
            return False, "Error: Library name cannot be empty."

        # Check for duplicate ID
        for lib in self.libraries:
            if lib["library_id"].lower() == library_id.lower():
                return False, f"Error: Library ID '{library_id}' already exists."

        # Add and save
        new_library = {
            "library_id": library_id,
            "library_name": library_name,
        }
        self.libraries.append(new_library)
        csv_storage.save_libraries(self.libraries)
        return True, f"Success: Library '{library_name}' (ID: {library_id}) added."

    def get_all_libraries(self):
        """
        Return a list of all libraries.

        Returns:
            list[dict]: All library records.
        """
        return self.libraries

    def library_exists(self, library_id):
        """
        Check whether a library with the given ID exists.

        Args:
            library_id (str): The library ID to look up.

        Returns:
            bool: True if the library exists, False otherwise.
        """
        for lib in self.libraries:
            if lib["library_id"].lower() == library_id.strip().lower():
                return True
        return False

    def get_library_name(self, library_id):
        """
        Get the name of a library by its ID.

        Args:
            library_id (str): The library ID.

        Returns:
            str: Library name, or "Unknown" if not found.
        """
        for lib in self.libraries:
            if lib["library_id"].lower() == library_id.strip().lower():
                return lib["library_name"]
        return "Unknown"

    # ------------------------------------------------------------------
    # Book operations
    # ------------------------------------------------------------------
    def add_book(self, book_id, title, author, isbn, publication_year, library_id):
        """
        Add a new book to a specific library after validation.

        Args:
            book_id (str): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            isbn (str): ISBN number.
            publication_year (str): Year of publication.
            library_id (str): ID of the library this book belongs to.

        Returns:
            tuple: (success: bool, message: str)
        """
        # Strip whitespace
        book_id = book_id.strip()
        title = title.strip()
        author = author.strip()
        isbn = isbn.strip()
        publication_year = publication_year.strip()
        library_id = library_id.strip()

        # Validate required fields
        if not book_id:
            return False, "Error: Book ID cannot be empty."
        if not title:
            return False, "Error: Book title cannot be empty."
        if not author:
            return False, "Error: Author cannot be empty."
        if not isbn:
            return False, "Error: ISBN cannot be empty."
        if not publication_year:
            return False, "Error: Publication year cannot be empty."
        if not library_id:
            return False, "Error: Library ID cannot be empty."

        # Validate publication year is a number
        if not publication_year.isdigit():
            return False, "Error: Publication year must be a number."

        year = int(publication_year)
        if year < 1000 or year > 2100:
            return False, "Error: Publication year must be between 1000 and 2100."

        # Check library exists
        if not self.library_exists(library_id):
            return False, f"Error: Library ID '{library_id}' does not exist. Add the library first."

        # Check for duplicate book ID
        for book in self.books:
            if book["book_id"].lower() == book_id.lower():
                return False, f"Error: Book ID '{book_id}' already exists."

        # Add and save
        new_book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "isbn": isbn,
            "publication_year": publication_year,
            "library_id": library_id,
        }
        self.books.append(new_book)
        csv_storage.save_books(self.books)
        return True, f"Success: Book '{title}' added to library '{self.get_library_name(library_id)}'."

    def get_books_by_library(self, library_id):
        """
        Return all books belonging to a specific library.

        Args:
            library_id (str): The library ID to filter by.

        Returns:
            list[dict]: Books in the specified library.
        """
        library_id = library_id.strip().lower()
        return [b for b in self.books if b["library_id"].lower() == library_id]

    def get_all_books(self):
        """
        Return all books across all libraries.

        Returns:
            list[dict]: All book records.
        """
        return self.books

    def search_books(self, keyword):
        """
        Search books by title, author, or ISBN (case-insensitive).

        Args:
            keyword (str): The search term.

        Returns:
            list[dict]: Books matching the keyword.
        """
        keyword = keyword.strip().lower()
        results = []
        for book in self.books:
            if (keyword in book["title"].lower()
                    or keyword in book["author"].lower()
                    or keyword in book["isbn"].lower()):
                results.append(book)
        return results

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    @staticmethod
    def format_library_table(libraries):
        """
        Format a list of libraries as a readable table string.

        Args:
            libraries (list[dict]): Library records.

        Returns:
            str: Formatted table.
        """
        if not libraries:
            return "  No libraries found."

        header = f"  {'Library ID':<15} {'Library Name':<30}"
        separator = "  " + "-" * 45
        lines = [header, separator]
        for lib in libraries:
            lines.append(f"  {lib['library_id']:<15} {lib['library_name']:<30}")
        return "\n".join(lines)

    def format_book_table(self, books):
        """
        Format a list of books as a readable table string.

        Args:
            books (list[dict]): Book records.

        Returns:
            str: Formatted table.
        """
        if not books:
            return "  No books found."

        header = (
            f"  {'Book ID':<10} {'Title':<25} {'Author':<20} "
            f"{'ISBN':<15} {'Year':<6} {'Library':<15}"
        )
        separator = "  " + "-" * 91
        lines = [header, separator]
        for book in books:
            lib_name = self.get_library_name(book["library_id"])
            lines.append(
                f"  {book['book_id']:<10} {book['title']:<25} {book['author']:<20} "
                f"  {book['isbn']:<15} {book['publication_year']:<6} {lib_name:<15}"
            )
        return "\n".join(lines)
