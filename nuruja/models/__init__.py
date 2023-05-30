import pendulum

from ..database import db


class CRUDMixin(object):
    """
    Mixin that offers functionality common to most, if not all of the models
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls, id: int):
        if any((isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))), ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self, commit: bool = True):
        db.session.add(self)

        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool = True, **kwargs):
        db.session.delete(self)

        if commit:
            db.session.commit()
        return self

    def update(self, commit: bool = True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self


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

    def __init__(self, username: str, email: str, phone_number: str, address: str, is_admin: bool = False) -> None:
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.is_admin = is_admin

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(db.Model, CRUDMixin):
    __tablename__ = "book"

    title = db.Column(db.String(100), nullable=False, unique=False)
    author = db.Column(db.String(120), nullable=False, unique=False)
    isbn = db.Column(db.String(120), nullable=False, unique=True)
    date_of_publication = db.Column(db.DateTime, nullable=False, unique=False, default=pendulum.now)

    # TODO: Implement categories as a relationship
    category = db.relationship("Category")
    status = db.Column(db.String(15), nullable=False, unique=False, default="not-rented")

    def __init__(self, title: str, author: str, isbn: str, date_of_publication: pendulum.DateTime,
                 category: str, status: str = "not-rented") -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.date_of_publication = date_of_publication
        self.category = category
        self.status = status

    def __repr__(self) -> str:
        return f"<Book {self.title} - {self.author}>"


class Category(db.Model, CRUDMixin):
    __tablename__ = "category"

    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True, unique=False)

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Shelf(db.Model, CRUDMixin):
    __tablename__ = "shelf"

    floor = db.Column(db.String(10), nullable=True, unique=True)
    book_id = db.relationship("Book")

    def __init__(self, floor: str):
        self.floor = floor

    def __repr__(self) -> str:
        return f"<Shelf {self.floor}>"


class Borrowing(db.Model, CRUDMixin):
    __tablename__ = "borrowing"

    user_id = db.relationship("User")
    book_id = db.relationship("Book")
    rent_fee = db.Column(db.Float, default=100, nullable=False, unique=False)
    is_return = db.Column(db.Boolean, default=False, nullable=False, unique=False)

# class Order(db.Model, CRUDMixin):
# class Transaction(db.Model, CRUDMixin)
