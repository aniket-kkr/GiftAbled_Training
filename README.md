# Library Management System

A beginner-friendly, command-line **Library Management System** built with Python 3 and CSV storage. This project allows you to manage multiple libraries, add books to each library, search across all libraries, and persist all data to CSV files.

---

## Features

- **Multiple Libraries** — Create and manage multiple libraries, each with a unique ID.
- **Book Management** — Add books with title, author, ISBN, and publication year to any library.
- **Search** — Search books by title, author, or ISBN (case-insensitive).
- **CSV Persistence** — All data is saved to `data/libraries.csv` and `data/books.csv`.
- **Input Validation** — Prevents duplicate IDs, empty fields, and invalid years.
- **Graceful Error Handling** — Handles missing files, empty CSVs, and invalid menu input.

---

## Prerequisites

- **Python 3.6+** (no external packages required)
- **Git** (for version control)

Check your Python version:
```bash
python --version
```

---

## Project Structure

```
Library/
├── main.py                # Entry point — CLI menu
├── library_manager.py     # Business logic (LibraryManager class)
├── csv_storage.py         # CSV read/write helpers
├── data/
│   ├── libraries.csv      # Persisted library records
│   └── books.csv          # Persisted book records
├── tests/
│   └── test_library.py    # Unit tests
├── README.md
├── .gitignore
└── requirements.txt
```

---

## Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/aniket-kkr/GiftAbled_Training.git
cd GiftAbled_Training
```

### 2. Run the application
```bash
python main.py
```

The `data/` directory and CSV files will be created automatically on first run.

---

## Example Usage

```
==================================================
       LIBRARY MANAGEMENT SYSTEM
==================================================
  1. Add Library
  2. View All Libraries
  3. Add Book
  4. View Books in a Library
  5. View All Books
  6. Search Books
  7. Display CSV Data
  8. Exit
==================================================
Enter your choice (1-8): 1

--- Add New Library ---
Enter Library ID: L1
Enter Library Name: City Library
Success: Library 'City Library' (ID: L1) added.

Enter your choice (1-8): 3

--- Add New Book ---
Available Libraries:
  Library ID      Library Name
  ---------------------------------------------
  L1              City Library

Enter Library ID to add the book to: L1
Enter Book ID: B1
Enter Book Title: Learn Python
Enter Author: Guido van Rossum
Enter ISBN: 978-0-13-467941-1
Enter Publication Year: 2020
Success: Book 'Learn Python' added to library 'City Library'.

Enter your choice (1-8): 6

--- Search Books ---
Enter search keyword (title / author / ISBN): Python

Search results for 'Python':
  Book ID    Title                     Author               ISBN            Year   Library
  -------------------------------------------------------------------------------------------
  B1         Learn Python              Guido van Rossum       978-0-13-467941-1 2020   City Library
```

---

## CSV Storage

All data is stored in plain CSV files inside the `data/` directory:

### `data/libraries.csv`
| Column       | Description              |
|-------------|--------------------------|
| library_id  | Unique library identifier |
| library_name| Name of the library       |

### `data/books.csv`
| Column           | Description                   |
|-----------------|-------------------------------|
| book_id         | Unique book identifier         |
| title           | Book title                     |
| author          | Book author                    |
| isbn            | ISBN number                    |
| publication_year| Year of publication            |
| library_id      | ID of the library it belongs to|

The CSV files are created automatically when the program runs for the first time.

---

## Running Tests

Run the test suite with:
```bash
python -m pytest tests/ -v
```

Or using the built-in `unittest` runner:
```bash
python -m unittest discover tests -v
```

The tests cover:
- Creating single and multiple libraries
- Adding books to different libraries
- Duplicate ID prevention
- Empty/invalid input validation
- Publication year validation
- Search by title, author, and ISBN
- Data persistence across restarts
- Missing/empty CSV file handling

---

## Technologies Used

- **Python 3** — Core language
- **csv module** — Built-in CSV file handling (no external dependencies)
- **unittest** — Built-in test framework
- **Git & GitHub** — Version control

---

## License

This project is created as part of the GiftAbled Agentic AI training program.
