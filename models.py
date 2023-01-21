import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id_publisher = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=70), unique=True)

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    id_book = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=70), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id_publisher"), nullable=False)

    publisher = relationship(Publisher, back_populates="books")
    stock = relationship('Stock', back_populates="book_s")


class Shop(Base):
    __tablename__ = "shop"

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=70), unique=True)

    stock_s = relationship("Stock", back_populates="shops")


class Stock(Base):
    __tablename__ = "stock"

    id_stock = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id_shop"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id_book"), nullable=False)

    shops = relationship("Shop", back_populates="stock_s")
    book_s = relationship("Book", back_populates="stock")
    sale = relationship("Sale", back_populates="stocks_sale")


class Sale(Base):
    __tablename__ = "sale"

    id_sale = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id_stock"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stocks_sale = relationship("Stock", back_populates="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
