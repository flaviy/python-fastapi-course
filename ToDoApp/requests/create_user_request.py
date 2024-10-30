from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=50)
    first_name: str = Field(min_length=3, max_length=150)
    last_name: str = Field(min_length=3, max_length=150)
    role: str = Field(min_length=3, max_length=150)
    is_active: bool = Field(default=True)
    phone_number: str = Field(min_length=6, max_length=14)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john_doe@gail.com",
                "username": "john_doe",
                "password": "password",
                "first_name": "John",
                "last_name": "Doe",
                "role": "admin",
                "is_active": True,
                "phone_number": "1234567890"
            }
        }
    }
