import os 
import datetime
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import db
from models import User, Book, Bookrental, Comment
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if not session.get('logged_in'):
	    return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET','POST'])  
def login():
    if request.method =='GET':
        return render_template('index.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')

        data_email=User.query.filter_by(email=email).first() 

        if check_password_hash(data_email.password, password):
            session['logged_in'] = email
            return ''' <script> alert('{}님 환영합니다'); location.href="/main" </script> '''.format(data_email.username)
        elif data_email is None:
            return ''' <script> alert('이메일이 틀렸습니다'); location.href="/login" </script> '''
        else:
            return ''' <script> alert('비밀번호가 틀렸습니다' ); location.href="/login" </script> '''


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return ''' <script> alert('로그아웃 되었습니다' ); location.href="/" </script> '''


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
            return ''' <script> alert("입력되지 않은 정보가 있습니다"); location.href="/register" </script> '''
        elif password != password_2:
            return ''' <script> alert("비밀번호가 일치하지 않습니다"); location.href="/register" </script> '''
        else:
            hashed_pw = generate_password_hash(password, method="sha256")
            usertable=User(
                username = username,
                email = email,
                password = hashed_pw
                
            )
            
            
            db.session.add(usertable)
            db.session.commit()
            return ''' <script> alert("{}님 회원가입 되었습니다"); location.href="/" </script> '''.format(username)
        return redirect('/')



@app.route('/main', methods=['GET','POST']) 
def main():
    books = Book.query.all()
    
    if request.method == 'GET':
        try:
            if session['logged_in'] is not None:
                return render_template('main.html', books=books)
        except:
            return ''' <script> alert("로그인을 하세요"); location.href="/" </script> '''
    else:
        book_id=request.form['book_id']

        data_book = Book.query.filter_by(id = book_id).first()
        data_user = User.query.filter_by(email=session['logged_in']).first()
        data_rentalbook=Bookrental.query.filter_by(book_id=data_book.id).first()

        
        if data_book.quantity<=0:
            return ''' <script> alert("대여할 수 없습니다"); location.href="/main" </script> '''
        
        elif db.session.query(Bookrental).filter(Bookrental.return_date.like('미반납')).count()>2:
                return ''' <script> alert("최대 3권만 빌릴 수 있습니다"); location.href="/main" </script> '''
 
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
            return ''' <script> alert("대여되었습니다"); location.href="/main" </script> '''
        return render_template('main.html', books=books)


@app.route('/BookRental', methods=['GET','POST']) 
def BookRental():
    data_user=User.query.filter_by(email=session['logged_in']).first()
    rentalbooks = Bookrental.query.filter_by(user_id=data_user.id)
    return render_template('BookRental.html', rentalbooks=rentalbooks)


@app.route('/returnbook', methods=['GET','POST']) 
def returnbook():
    data_user=User.query.filter_by(email=session['logged_in']).first()
    returnbooks = Bookrental.query.filter_by(return_date='미반납', user_id=data_user.id)  #미반납인 책들만 출력
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
        return ''' <script> alert("반납되었습니다"); location.href="/returnbook" </script> '''

    return render_template('returnbook.html', returnbooks=returnbooks)


@app.route('/books/<int:book_id>/', methods=['GET','POST'])
def books(book_id):
    book = Book.query.filter_by(id=book_id).first()
    comments= Comment.query.filter_by(book_id=book_id).all()
    
    if request.method == 'GET':
        return render_template('bookdescript.html', book=book, comments=comments)
    else:

        data_user = User.query.filter_by(email=session['logged_in']).first()
        find_user = Comment.query.filter_by(user_id=data_user.id, book_id=book.id).first()

        if find_user is None:
            content=request.form['content']
            rating=int(request.form['rating'])+1


            comment= Comment(
                    book_id = book.id,
                    user_id = data_user.id,
                    content = content,
                    rating = rating,
                    create_date = datetime.datetime.now()
                )
            db.session.add(comment)
            db.session.commit()



            return render_template('bookdescript.html', book=book, comments=comments)
        else:
            return ''' <script> alert("댓글은 한번만 입력 가능합니다"); location.href="/books/{}/" </script> '''.format(book.id)


if __name__ == "__main__":

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/library'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'manyrandombyte'

    db.init_app(app) 
    db.app = app
    db.create_all() 

    app.run(host="0.0.0.0", port=5000, debug=True)
