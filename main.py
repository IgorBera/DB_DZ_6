import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import json
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
DBMS = os.getenv('DBMS')
user_name = os.getenv('USER_NAME')
user_password = os.getenv('USER_PASSWORD')
host = os.getenv('HOST')
name_DB = os.getenv('NAME_DB')

DSN = f"{DBMS}://{user_name}:{user_password}@{host}/{name_DB}"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('test_data.json', encoding='utf-8') as data:
    data = json.load(data)
    for row in data:
        if 'publisher' in row.values():
            s = Publisher(name=row['fields']['name'])
        if 'book' in row.values():
            s = Book(title=row['fields']['title'], id_publisher=row['fields']['id_publisher'])
        if 'shop' in row.values():
            s = Shop(name=row['fields']['name'])
        if 'stock' in row.values():
            s = Stock(count=row['fields']['count'], id_book=row['fields']['id_book'],
                      id_shop=row['fields']['id_shop'])
        if 'sale' in row.values():
            s = Sale(price=row['fields']['price'], date_sale=row['fields']['date_sale'],
                     count=row['fields']['count'], id_stock=row['fields']['id_stock'])
        session.add(s)
        session.commit()


def get_publisher_sales():
    id_or_name = input("Введите id или имя издателя: ")
    if id_or_name.isnumeric():
        for row in session.query(Book.title, Shop.name, (Sale.price * Sale.count), Sale.date_sale)\
                .join(Stock.book_s).join(Stock.shops).join(Stock.sale)\
                .filter(Book.id_publisher == id_or_name):
            print(row)
    else:
        for row in session.query(Book.title, Shop.name, (Sale.price * Sale.count), Sale.date_sale)\
                .join(Stock.book_s).join(Stock.shops).join(Book.publisher).join(Stock.sale)\
                .filter(Publisher.name.like(id_or_name)):
            print(row)


get_publisher_sales()
session.close()
