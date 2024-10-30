import pytest


class Student:
    def __init__(self, first_name: str, last_name: str, age: int, major: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.major = major


@pytest.fixture
def default_employee():
    return Student("John", "Doe", 25, "Computer Science")


def test_initialization(default_employee):
    assert default_employee.first_name == "John"
    assert default_employee.last_name == "Doe"
    assert default_employee.age == 25
    assert default_employee.major == "Computer Science"
