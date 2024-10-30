"""
uvicorn main:app --reload - to refresh the server every time you make a change
to run production instance :
fastapi run main.py

"""


from fastapi import FastAPI

from books import books_endpoints, books2_endpoints

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

books_endpoints.init_book_endpoints(app)
books2_endpoints.init_book_endpoints(app)
