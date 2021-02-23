import os #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('login.html')

@app.route('/register', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password')

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

if __name__ == "__main__":
    #데이터베이스---------
 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/library?charset=utf8'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'manyrandombyte'

#    db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    app.run(host="127.0.0.1", port=5000, debug=True)