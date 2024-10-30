from datetime import date


class Book:

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
