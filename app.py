import os #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User, Book
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('login.html')

@app.route('/login', methods=['GET','POST'])  
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')

        data=User.query.filter_by(email=email, password=password).first() 

        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            return 'Dont Login' 


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
            usertable=User() #user_table 클래스
            usertable.username = username
            usertable.email = email
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()
            return "회원가입 성공"
        return redirect('/')


@app.route('/main', methods=['GET','POST']) 
def main():
    if request.method == 'GET':
        return render_template("main.html")
    else:
        return render_template("main.html")





if __name__ == "__main__":

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/library'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'manyrandombyte'


    db.init_app(app) 
    db.app = app
    db.create_all() 

    app.run(host="127.0.0.1", port=5000, debug=True)