from typing import Optional

from pendulum import DateTime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserSchema(BaseSchema):
    id: int
    username: str
    email: str
    phone_number: str
    address: str
    is_admin: Optional[bool] = False


class AllUsersSchema(BaseSchema):
    users: Optional[list[UserSchema]]


class UserUpdateSchema(BaseSchema):
    username: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    is_admin: Optional[bool] = False


class BookSchema(BaseSchema):
    id: int
    title: str
    author: str
    isbn: str
    date_of_publication: DateTime
    category: Optional[str]
    status: str
    rent_fee: int
    late_penalty_fee: int


class AllBooksSchema(BaseSchema):
    books: list[BookSchema]


class BorrowBookSchema(BaseSchema):
    book_id: int
