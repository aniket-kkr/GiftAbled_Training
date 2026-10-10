"""
csv_storage.py - Handles reading and writing data to CSV files.

This module provides functions to load and save libraries and books
using Python's built-in csv module. It automatically creates the
data directory and CSV files if they do not exist.
"""

import csv
import os


# ---------------------------------------------------------------------------
# Path configuration (relative to this file's directory)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

LIBRARIES_CSV = os.path.join(DATA_DIR, "libraries.csv")
BOOKS_CSV = os.path.join(DATA_DIR, "books.csv")

# CSV column headers
LIBRARY_FIELDS = ["library_id", "library_name"]
BOOK_FIELDS = ["book_id", "title", "author", "isbn", "publication_year", "library_id"]


# ---------------------------------------------------------------------------
# Helper: ensure the data directory and CSV files exist
# ---------------------------------------------------------------------------
def _ensure_data_files():
    """Create the data/ directory and empty CSV files if they are missing."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create libraries.csv with headers if it doesn't exist or is empty
    if not os.path.exists(LIBRARIES_CSV) or os.path.getsize(LIBRARIES_CSV) == 0:
        with open(LIBRARIES_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LIBRARY_FIELDS)
            writer.writeheader()

    # Create books.csv with headers if it doesn't exist or is empty
    if not os.path.exists(BOOKS_CSV) or os.path.getsize(BOOKS_CSV) == 0:
        with open(BOOKS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOK_FIELDS)
            writer.writeheader()


# ---------------------------------------------------------------------------
# Library CSV operations
# ---------------------------------------------------------------------------
def load_libraries():
    """
    Read all libraries from libraries.csv and return them as a list of dicts.

    Returns:
        list[dict]: Each dict has keys 'library_id' and 'library_name'.
    """
    _ensure_data_files()
    libraries = []
    try:
        with open(LIBRARIES_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                libraries.append(row)
    except Exception as e:
        print(f"Warning: Could not read libraries file - {e}")
    return libraries


def save_libraries(libraries):
    """
    Write the full list of library dicts to libraries.csv (overwrite).

    Args:
        libraries (list[dict]): Each dict must have 'library_id' and 'library_name'.
    """
    _ensure_data_files()
    try:
        with open(LIBRARIES_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=LIBRARY_FIELDS)
            writer.writeheader()
            writer.writerows(libraries)
    except Exception as e:
        print(f"Error: Could not save libraries - {e}")


# ---------------------------------------------------------------------------
# Book CSV operations
# ---------------------------------------------------------------------------
def load_books():
    """
    Read all books from books.csv and return them as a list of dicts.

    Returns:
        list[dict]: Each dict has keys matching BOOK_FIELDS.
    """
    _ensure_data_files()
    books = []
    try:
        with open(BOOKS_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(row)
    except Exception as e:
        print(f"Warning: Could not read books file - {e}")
    return books


def save_books(books):
    """
    Write the full list of book dicts to books.csv (overwrite).

    Args:
        books (list[dict]): Each dict must have keys matching BOOK_FIELDS.
    """
    _ensure_data_files()
    try:
        with open(BOOKS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOK_FIELDS)
            writer.writeheader()
            writer.writerows(books)
    except Exception as e:
        print(f"Error: Could not save books - {e}")
