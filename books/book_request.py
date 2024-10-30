from typing import Optional

from pydantic import BaseModel, Field
from datetime import date

class BookRequest(BaseModel):
    #id: Optional[int] = None
    id: Optional[int] = Field(description="ID is not needed on create!!!", default=None)
    title: str = Field(min_length=3, max_length=150)
    author: str
    description: str
    rating: int = Field(ge=1, le=5)
    published_date: Optional[date] = Field(description="YYYY-MM-DD", default=None, gt="1900-01-01", lt=date.today())

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Harry Potter",
                "author": "J.K. Rowling",
                "description": "fantasy",
                "rating": 5,
                "published_date": "2024-01-01"
            }
        }
    }
