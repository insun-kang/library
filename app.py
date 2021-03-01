import os 
import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User, Book, Bookrental

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if not session.get('logged_in'):
	    return render_template('index2.html')
    else:
        return render_template('index2.html')

@app.route('/login', methods=['GET','POST'])  
def login():
    if request.method =='GET':
        return render_template('index.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')

        data_email=User.query.filter_by(email=email).first() 
        data_password=User.query.filter_by(password=password).first()

        if data_email is not None and data_password is not None:
            session['logged_in'] = email
            return redirect(url_for('main'))
        elif data_email is None:
            return '이메일이 틀렸습니다'
        else:
            return '비밀번호가 틀렸습니다' 

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET','POST']) 
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('re_password')

        if not(username and email and password and password_2):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            usertable=User(
                username = username,
                email = email,
                password = password
                
            )
            
            
            db.session.add(usertable)
            db.session.commit()
            return "회원가입 성공"
        return redirect('/')


@app.route('/main', methods=['GET','POST']) 
def main():
    books = Book.query.all()
    
    if request.method == 'GET':
        return render_template('main.html', books=books)
    else:
        book_id=request.form['book_id']

        data_book = Book.query.filter_by(id = book_id).first()
        data_user = User.query.filter_by(email=session['logged_in']).first()
        data_rentalbook=Bookrental.query.filter_by(book_id=data_book.id).first()

        if data_book.quantity<=0:
            return '대여할 수 없습니다.'

 
        else:
            data_book.quantity -= 1

            bookrental= Bookrental(
                book_id=data_book.id,
                bookname=data_book.book_name,
                user_id=data_user.id,
                username=data_user.username,
                rental_date=datetime.date.today(),
                return_date='미반납'
            )
            db.session.add(bookrental)
            db.session.commit()
            return '대여성공'
        return render_template('main.html', books=books)

@app.route('/BookRental', methods=['GET','POST']) 
def BookRental():
    rentalbooks = Bookrental.query.all()
    return render_template('BookRental.html', rentalbooks=rentalbooks)

@app.route('/returnbook', methods=['GET','POST']) 
def returnbook():
    returnbooks = Bookrental.query.filter_by(return_date='미반납')  #미반납인 책들만 출력
    if request.method == 'GET':
        return render_template('returnbook.html', returnbooks=returnbooks)
    else:
        bookname=request.form['bookname']
        data_returnbook=Bookrental.query.filter_by(bookname=bookname).all()   #반납시 현재시간 return_date에 삽입
        data_returnbook[-1].return_date=datetime.date.today()
        db.session.commit()


        data_book = Book.query.filter_by(book_name = bookname).first()  #반납시 수량 +1
        data_book.quantity += 1
        db.session.commit()


    return render_template('returnbook.html', returnbooks=returnbooks)

@app.route('/books/<int:id>/')
def books(id):
    book = Book.query.get(id)
    return render_template('bookdescript.html', book=book)


if __name__ == "__main__":

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/library'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'manyrandombyte'

    db.init_app(app) 
    db.app = app
    db.create_all() 

    app.run(host="127.0.0.1", port=80, debug=True)