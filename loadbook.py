import csv
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

from models import Book
from models import create_app
from app import db

app = create_app()
app.app_context().push()

session = db.session


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/library'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



with open('booklist.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        published_at = datetime.strptime(
						row['publication_date'], '%Y-%m-%d').date()
        image_path = f"/static/image/{row['id']}"
        try:
            open(f'app/{image_path}.png')
            image_path += '.png'
        except:
            image_path += '.jpg'

        book = Book(
            id=int(row['id']), 
            book_name=row['book_name'], 
            publisher=row['publisher'],
            author=row['author'], 
            published_at=published_at, 
            pages=int(row['pages']),
            isbn=row['isbn'], 
            description=row['description'], 
            image_path=image_path,
            quantity=5,
            rating=0,
        )
        db.session.add(book)

    db.session.commit()

