# A15 - Library Web Page with CRUD

A full CRUD web page and REST API for managing a library's book catalog, inventory, and borrower actions (borrow / return) built with FastAPI and vanilla JavaScript.

## Features
- **Add Book**: Add new books with validation (title, author, genre, ISBN, publication year, total copies).
- **View Catalog**: Search by title, author, or ISBN, with genre filtering and real-time inventory counters.
- **Update Book**: Edit existing book details via a modal form.
- **Delete Book**: Remove obsolete books from the catalog.
- **Borrow / Return System**:
  - Click "Borrow" to decrement available copies (disables when out of stock).
  - Click "Return" to increment available copies back up to total capacity.
- **Real-time Inventory Metrics**: Total titles, total physical copies, available copies, and borrowed copies.

## Run
Install requirements and launch the server:

```bash
pip install -r requirements.txt
python main.py
```

Then visit:
`http://127.0.0.1:8000`
