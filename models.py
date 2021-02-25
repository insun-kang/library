from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, url_for
db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    return app

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'usertable' #테이블 이름
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)


    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User(email='%s', username='%s')>" % (self.email, self.username)

class Book(db.Model):
    __tablename__ = 'booktable'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id=db.Column(db.Integer, primary_key=True)
    book_name=db.Column(db.String(100))
    publisher =db.Column(db.String(100))
    author =db.Column(db.String(100))
    published_at=db.Column(db.String(100))
    pages=db.Column(db.String(100))
    isbn =db.Column(db.String(100))
    description=db.Column(db.String(1000))
    image_path = db.Column(db.String(500))
    quantity=db.Column(db.String(8))
    rating=db.Column(db.String(8))

    def __init__(self, id, book_name, publisher, author, published_at, pages, isbn, description, image_path, quantity, rating):
        self.id=id
        self.book_name=book_name
        self.publisher=publisher
        self.author=author
        self.published_at=published_at
        self.pages=pages
        self.isbn=isbn
        self.description=description
        self.imange_path=image_path
        self.quantity=quantity
        self.rating=rating

    def __str__(self):
        return f"book_name : '{self.book_name}'"
    