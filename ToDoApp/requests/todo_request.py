from typing import Optional

from pydantic import BaseModel, Field
from datetime import date

class TodoRequest(BaseModel):
    #id: Optional[int] = None
    id: Optional[int] = Field(description="ID is not needed on create!!!", default=None)
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=3, max_length=150)
    priority: int = Field(ge=1, le=5)
    complete: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Read a book",
                "description": "Read Harry Potter",
                "priority": 5,
                "complete": False
            }
        }
    }
