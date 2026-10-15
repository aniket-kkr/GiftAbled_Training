from book import Book
from library import Library


def main():
    library = Library()
    library.add_book(Book("Python Basics", "Alex", 2))
    library.add_book(Book("Clean Code", "Robert C. Martin", 1))
    library.show_books()

    library.save_json()
    library.export_csv()

    try:
        library.borrow_book("Python Basics")
        library.return_book("Python Basics")
    except (KeyError, ValueError) as e:
        print("Library error:", e)

    restored = Library()
    restored.load_json()
    print("\\nLoaded from JSON:")
    restored.show_books()


if __name__ == "__main__":
    main()
