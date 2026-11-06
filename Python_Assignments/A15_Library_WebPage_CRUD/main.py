from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="Library Book Management | CRUD Web Application",
    description="Assignment 15: Library Web Page with CRUD for books",
    version="1.0.0",
)

html_file = Path(__file__).with_name("index.html")


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., min_length=5, max_length=30)
    publication_year: int = Field(..., ge=1000, le=2050)
    genre: str = Field(..., min_length=2, max_length=50)
    total_copies: int = Field(..., ge=1, le=1000)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=5, max_length=30)
    publication_year: Optional[int] = Field(None, ge=1000, le=2050)
    genre: Optional[str] = Field(None, min_length=2, max_length=50)
    total_copies: Optional[int] = Field(None, ge=1, le=1000)


class Book(BookBase):
    id: int
    available_copies: int


# Initial Seed Library
BOOKS_DB: List[Book] = [
    Book(id=1, title="Fluent Python", author="Luciano Ramalho", isbn="978-1491946008", publication_year=2022, genre="Programming", total_copies=5, available_copies=4),
    Book(id=2, title="Clean Code", author="Robert C. Martin", isbn="978-0132350884", publication_year=2008, genre="Software Engineering", total_copies=3, available_copies=1),
    Book(id=3, title="Introduction to Algorithms", author="Thomas H. Cormen", isbn="978-0262033848", publication_year=2009, genre="Computer Science", total_copies=4, available_copies=3),
    Book(id=4, title="Python Crash Course", author="Eric Matthes", isbn="978-1593279288", publication_year=2019, genre="Programming", total_copies=6, available_copies=6),
    Book(id=5, title="Design Patterns", author="Erich Gamma et al.", isbn="978-0201633610", publication_year=1994, genre="Architecture", total_copies=2, available_copies=0),
]
next_book_id = 6


@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(html_file, media_type="text/html")


@app.get("/api/books", response_model=List[Book])
def get_books(
    search: Optional[str] = Query(None, description="Search by title, author, or ISBN"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
):
    results = BOOKS_DB
    if search:
        s = search.lower()
        results = [
            b for b in results
            if s in b.title.lower() or s in b.author.lower() or s in b.isbn.lower()
        ]
    if genre and genre != "All":
        results = [b for b in results if b.genre.lower() == genre.lower()]
    return results


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for b in BOOKS_DB:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/api/books", response_model=Book, status_code=201)
def add_book(payload: BookCreate):
    global next_book_id
    # Check for duplicate ISBN
    for b in BOOKS_DB:
        if b.isbn.strip().lower() == payload.isbn.strip().lower():
            raise HTTPException(status_code=400, detail="A book with this ISBN already exists")

    new_book = Book(
        id=next_book_id,
        title=payload.title.strip(),
        author=payload.author.strip(),
        isbn=payload.isbn.strip(),
        publication_year=payload.publication_year,
        genre=payload.genre.strip(),
        total_copies=payload.total_copies,
        available_copies=payload.total_copies,
    )
    BOOKS_DB.append(new_book)
    next_book_id += 1
    return new_book


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate):
    for i, b in enumerate(BOOKS_DB):
        if b.id == book_id:
            updated_dict = b.model_dump()
            if payload.title is not None:
                updated_dict["title"] = payload.title.strip()
            if payload.author is not None:
                updated_dict["author"] = payload.author.strip()
            if payload.isbn is not None:
                updated_dict["isbn"] = payload.isbn.strip()
            if payload.publication_year is not None:
                updated_dict["publication_year"] = payload.publication_year
            if payload.genre is not None:
                updated_dict["genre"] = payload.genre.strip()
            if payload.total_copies is not None:
                diff = payload.total_copies - b.total_copies
                updated_dict["total_copies"] = payload.total_copies
                updated_dict["available_copies"] = max(0, b.available_copies + diff)

            updated_book = Book(**updated_dict)
            BOOKS_DB[i] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(BOOKS_DB):
        if b.id == book_id:
            deleted = BOOKS_DB.pop(i)
            return {"message": f"Book '{deleted.title}' deleted successfully", "id": book_id}
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/api/books/{book_id}/borrow")
def borrow_book(book_id: int):
    for b in BOOKS_DB:
        if b.id == book_id:
            if b.available_copies <= 0:
                raise HTTPException(status_code=400, detail="No copies currently available to borrow")
            b.available_copies -= 1
            return {"message": f"Successfully borrowed 1 copy of '{b.title}'", "available_copies": b.available_copies}
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/api/books/{book_id}/return")
def return_book(book_id: int):
    for b in BOOKS_DB:
        if b.id == book_id:
            if b.available_copies >= b.total_copies:
                raise HTTPException(status_code=400, detail="All copies are already returned for this book")
            b.available_copies += 1
            return {"message": f"Successfully returned 1 copy of '{b.title}'", "available_copies": b.available_copies}
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/api/stats")
def get_stats():
    total_titles = len(BOOKS_DB)
    total_copies = sum(b.total_copies for b in BOOKS_DB)
    available_copies = sum(b.available_copies for b in BOOKS_DB)
    borrowed_copies = total_copies - available_copies
    genres = sorted(list({b.genre for b in BOOKS_DB}))

    return {
        "total_titles": total_titles,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "borrowed_copies": borrowed_copies,
        "genres": genres,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
