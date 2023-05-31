from typing import Optional

from pendulum import DateTime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserSchema(BaseSchema):
    username: str
    email: str
    phone_number: str
    address: str
    is_admin: Optional[bool] = False


class UserUpdateSchema(BaseSchema):
    username: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool] = False


class BookSchema(BaseSchema):
    title: str
    author: str
    isbn: str
    date_of_publication: DateTime
    category: Optional[str]
    status: str


class AllBooksSchema(BaseSchema):
    books: list[BookSchema]


class BorrowBookSchema(BaseSchema):
    book_id: int
    rent_fee: float


class ReturnBookSchema(BaseSchema):
    book_id: int
