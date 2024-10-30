from fastapi import APIRouter, Body

router = APIRouter()

books = [
    {"title": "Harry Potter", "author": "J.K. Rowling", "category": "fantasy"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "fantasy"},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "category": "mystery"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "adventure"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "fiction"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "fiction"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "fiction"},
    {"title": "1984", "author": "George Orwell", "category": "fiction"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "romance"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "fantasy"},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "category": "dystopian"},
]


# using .get() method is defensive programming practice
# it will return None if the key is not found
# instead of raising an exception
# when dealing with url %20 is a space
@router.get("/books/read/{book_title}")
async def read_book(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


@router.get("/books/read-all")
async def read_all_books():
    return books


# using query parameters
@router.get("/books/")
async def read_category_books(category: str):
    return [book for book in books if book.get('category').casefold() == category.casefold()]


@router.get("/books/{author}")
async def read_author_books(author: str, category: str):
    books_result = []
    for book in books:
        if (book.get('author').casefold() == author.casefold() and
                book.get('category').casefold() == category.casefold()):
            books_result.append(book)
    return books_result


# book = {"title": "Harry Potter", "author": "J.K. Rowling", "category": "fantasy"}
@router.post("/books/create")
async def create_book(book=Body()):
    # check if the book already exists
    for b in books:
        if b.get('title').casefold() == book.get('title').casefold():
            return {"message": "Book already exists", "status": 400}
    # check that the book has all the required fields
    if not all(key in book for key in ['title', 'author', 'category']):
        return {"message": "Book is missing required fields", "status": 400}
    books.append(book)
    return books


@router.put("/books/update/{book_title}")
async def update_book(book_title: str, book=Body()):
    for b in books:
        if b.get('title').casefold() == book_title.casefold():
            b.update(book)
            return {"message": "Book updated"}
    return {"message": "Book not found"}


@router.delete("/books/delete/{book_title}")
async def delete_book(book_title: str):
    # for book in books:
    #     if book.get('title').casefold() == book_title.casefold():
    #         books.remove(book)
    #         return {"message": "Book deleted"}
    # return {"message": "Book not found"}

    # using list comprehension
    # books[:] = [book for book in books if book.get('title').casefold() != book_title.casefold()]
    # return {"message": "Book deleted"}

    for i in range(len(books)):
        if books[i].get('title').casefold() == book_title.casefold():
            books.pop(i)
            return {"message": "Book deleted"}


@router.get("/books/author/{author}")
async def read_author_books(author: str):
    return [book for book in books if book.get('author').casefold() == author.casefold()]


def init_book_endpoints(app):
    app.include_router(router)
