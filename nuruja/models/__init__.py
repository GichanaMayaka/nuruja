import pendulum

from .mixins import CRUDMixin
from ..extensions import db


class User(db.Model, CRUDMixin):
    """
    Represents a user
    """

    __tablename__ = "user"

    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False, unique=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationship[s]
    transactions = db.relationship("Transactions", back_populates="user")
    user_balance = db.relationship("UserBalance", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(db.Model, CRUDMixin):
    __tablename__ = "book"

    title = db.Column(db.String(100), nullable=False, unique=False)
    author = db.Column(db.String(120), nullable=False, unique=False)
    isbn = db.Column(db.String(120), nullable=False, unique=True)
    date_of_publication = db.Column(
        db.DateTime, nullable=False, unique=False, default=pendulum.now
    )
    status = db.Column(
        db.String(15), nullable=False, unique=False, default="not-rented"
    )
    rent_fee = db.Column(db.Integer, nullable=False, unique=False, default=100)
    late_penalty_fee = db.Column(db.Integer, nullable=False, unique=False, default=25)

    # Foreign Key[s]
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    # Relationship[s]
    category = db.relationship("Category", back_populates="book")
    transactions = db.relationship("Transactions", back_populates="book", uselist=False)
    shelf = db.relationship("Shelf", back_populates="book")

    def __repr__(self) -> str:
        return f"<Book {self.title} - {self.author}>"


class Category(db.Model, CRUDMixin):
    __tablename__ = "category"

    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True, unique=False)

    # Relationship[s]
    book = db.relationship("Book", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Shelf(db.Model, CRUDMixin):
    __tablename__ = "shelf"

    floor = db.Column(db.String(10), nullable=True, unique=False)

    # Foreign Key[s]
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete="CASCADE"))

    # Relationship[s]
    book = db.relationship("Book", back_populates="shelf")

    def __repr__(self) -> str:
        return f"<Shelf {self.floor}>"


class Transactions(db.Model, CRUDMixin):
    __tablename__ = "transactions"

    rent_fee = db.Column(db.Float, default=100, nullable=False, unique=False)
    is_return = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    date_borrowed = db.Column(
        db.DateTime, nullable=False, unique=False, default=pendulum.now
    )
    date_due = db.Column(
        db.DateTime,
        nullable=False,
        unique=False,
        default=pendulum.now() + pendulum.duration(days=14),
    )

    # Foreign Key[s]
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))

    # Relationship[s]
    book = db.relationship("Book", back_populates="transactions")
    user = db.relationship("User", back_populates="transactions")
    user_balance = db.relationship("UserBalance", backref="transactions")


class UserBalance(db.Model, CRUDMixin):
    __tablename__ = "user_balance"

    balance = db.Column(db.Float, nullable=False, unique=False, default=0)
    date_of_entry = db.Column(
        db.DateTime, nullable=False, unique=False, default=pendulum.now
    )

    # Foreign Key[s]
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    transaction_id = db.Column(db.Integer, db.ForeignKey("transactions.id"))

    # Relationship[s]
    user = db.relationship("User", back_populates="user_balance")
