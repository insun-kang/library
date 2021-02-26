from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

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
    email = db.Column(db.String(32))
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))


    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)


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
    quantity=db.Column(db.Integer, default=0)
    rating=db.Column(db.Integer, default=0)

class Bookrental(db.Model):
    __tablename__ = 'bookrentaltable'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id=db.Column(db.Integer, primary_key=True)
    book_id=db.Column(db.Integer, ForeignKey('booktable.id'))
    username= db.Column(db.String(32))
    rental_date=db.Column(db.DATE)
    return_date=db.Column(db.DATE, nullable=True)
