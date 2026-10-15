import csv
import json
from pathlib import Path
from book import Book


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        key = book.title.casefold()
        if key in self.books:
            self.books[key].add_copies(book.get_copies())
        else:
            self.books[key] = book

    def show_books(self):
        for book in self.books.values():
            print(book)

    def borrow_book(self, title):
        book = self.books.get(title.casefold())
        if book is None:
            raise KeyError(f"Book not found: {title}")
        if not book.borrow():
            raise ValueError(f"No copies available: {title}")
        return True

    def return_book(self, title):
        book = self.books.get(title.casefold())
        if book is None:
            raise KeyError(f"Book not found: {title}")
        book.return_copy()

    def save_json(self, filename="library.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books.values()], f, indent=2)

    def load_json(self, filename="library.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON must contain a list of books")
            loaded = [Book.from_dict(row) for row in data]
            self.books = {b.title.casefold(): b for b in loaded}
        except FileNotFoundError:
            raise
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise ValueError("Invalid library JSON") from e

    def export_csv(self, filename="library.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author", "copies"])
            writer.writeheader()
            for book in self.books.values():
                writer.writerow(book.to_dict())

    def read_text(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
