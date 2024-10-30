from fastapi import APIRouter, Body, Path, Query, HTTPException

from books.book import Book
from books.book_request import BookRequest
from starlette import status

router = APIRouter()

books = [
    Book(1, "Harry Potter", "J.K. Rowling", "fantasy", 5, "2024-01-01"),
    Book(2, "The Da Vinci Code", "Dan Brown", "mystery", 4, "2024-01-01"),
    Book(3, "The Alchemist", "Paulo Coelho", "adventure", 3, "2022-12-10"),
    Book(4, "The Catcher in the Rye", "J.D. Salinger", "fiction", 2, "2020-10-05"),
    Book(5, "The Great Gatsby", "F. Scott Fitzgerald", "fiction", 1, "2019-05-20"),
]


@router.get("/books2/read_all")
async def read_all_books():
    return books


@router.post("/books2/create")
async def create_book(body=Body()):
    book = Book(**body)
    books.append(book)
    return {"message": "Book created successfully", "status": 201}


@router.post("/books2/create_with_validation", status_code=status.HTTP_201_CREATED)
async def create_book_with_validation(book_request: BookRequest):
    book = Book(**book_request.model_dump())
    books.append(find_book_id(book))
    return {"message": "Book created successfully", "status": 201}


@router.get("/books2/{book_id}")
async def read_book(book_id: int =
                    Path(gt=0, description="The ID of the book you want to read", message="ID must be greater than 0")):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# using query parameters
@router.get("/books2/")
async def read_books_by_rating(rating: int = Query(message="Rating must be between 1 and 5", ge=1, le=5)):
    return [book for book in books if book.rating == rating]


@router.get("/books2/books_by_date_range")
async def read_books_by_published_date_range(start_date: str, end_date: str):
    return [book for book in books if start_date <= book.published_date <= end_date]


@router.put("/books2/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    for i in range(len(books)):
        if books[i].id == book_request.id:
            books[i] = Book(**book_request.model_dump())
            return {"message": "Book updated successfully", "status": 200}


@router.put("/books2/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int =
                      Path(gt=0,
                           description="The ID of the book you want to delete",
                           message="ID must be greater than 0")
                      ):
    for i in range(len(books)):
        if books[i].id == book_id:
            #del books[i]
            books.pop(i)
            return {"message": "Book deleted successfully", "status": 200}
    return {"message": "Book not found", "status": 404}


def find_book_id(book: Book):
    book.id = books[-1].id + 1 if len(books) > 0 else 1
    return book


def init_book_endpoints(app):
    app.include_router(router)
