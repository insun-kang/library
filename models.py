from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

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
        return '<User %r>' % self.username

class Book(db.Model):
    __tablename__ = 'booktable' #테이블 이름
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id=db.Column(db.Integer, primary_key=True)
    book_name=db.Column(db.String(100), unique=True, nullable=False)
    publisher =db.Column(db.String(100), unique=True, nullable=False)
    author =db.Column(db.String(100), unique=True, nullable=False)
    publication_date=db.Column(db.String(100), unique=True, nullable=False)
    pages=db.Column(db.String(100), unique=True, nullable=False)
    isbn =db.Column(db.String(100), unique=True, nullable=False)
    description=db.Column(db.String(100), unique=True, nullable=False)
    quantity=db.Column(db.String(8), unique=True, nullable=False)
    rating=db.Column(db.String(8), unique=True, nullable=False)

    def __init__(self, book_name, publisher, author, publication_date, pages, isbn, description, quantity, rating):
        self.book_name=book_name
        self.publisher=publisher
        self.author=author
        self.publication_date=publication_date
        self.pages=pages
        self.isbn=isbn
        self.description=description
        self.quantity=quantity
        self.rating=rating

    def __str__(self):
        return f"book_name : '{self.book_name}'"
    