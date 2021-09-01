# encoding: utf-8

from datetime import datetime
from flask import Flask,request,send_file
from flask_sqlalchemy import SQLAlchemy
from gevent import pywsgi


app = Flask(__name__,static_url_path="/registration/")
app.config['SQLALCHEMY_DATABASE_URI'] = '' #此处注意填写
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # name = db.Column(db.String(50), unique=True)
    # email = db.Column(db.String(120), unique=True)
    name=db.Column(db.String(50))
    sex=db.Column(db.String(1))
    studentID=db.Column(db.BigInteger)
    college=db.Column(db.String(10))
    classs=db.Column(db.String(20))
    qq=db.Column(db.BigInteger, unique=True)
    phoneNumber=db.Column(db.BigInteger)
    department1=db.Column(db.Integer)
    reason1=db.Column(db.String(500))
    department2=db.Column(db.Integer)
    reason2=db.Column(db.String(500))
    interest=db.Column(db.String(500))
    time=db.Column(db.String(50))
    ip=db.Column(db.String(50))

    def __init__(self, name,sex,studentID,college,classs,qq,phoneNumber,department1,reason1,department2,reason2,interest,time,ip ):
        self.name = name
        self.sex = sex
        self.studentID=int(studentID)
        self.college=college
        self.classs=classs
        self.qq=int(qq)
        self.phoneNumber=int(phoneNumber)
        self.department1=int(department1)
        self.reason1=reason1
        self.department2=int(department2)
        self.reason2=reason2
        self.interest=interest
        self.time=time
        self.ip=ip

    # def __repr__(self):
    #     return '<User %r>' % self.username

# 跨域支持
def after_request(response):
    #JS前端跨域支持
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

app.after_request(after_request)

@app.route('/registration/')
def index():
    return send_file("./static/RegistrationForm.html")

@app.route('/registration//submit',methods=['POST'])
def getIt():
    time=datetime.now().strftime('%m-%d %H:%M:%S')
    ip=request.headers['X-Forwarded-For']
    name=request.form.get("name")
    sex=request.form.get("sex")
    studentID=request.form.get("studentID")
    college=request.form.get("college")
    classs=request.form.get("class")
    qq=request.form.get("qq")
    phoneNumber=request.form.get("phoneNumber")
    department1=request.form.get("department1")
    reason1=request.form.get("reason1")
    department2=request.form.get("department2")
    reason2=request.form.get("reason2")
    interest=request.form.get("interest")
    if None in [name,sex,studentID,college,classs,qq,phoneNumber,department1,reason1,department2,reason2,interest] :
        return "error"
    if sex!="男" and sex!="女":
        return "error"
    if len(studentID)!=13:
        return "error"
    if department1=="0" and department2=="0":
        return "error"
    if department1 not in ["1","2","3","0"] or department2 not in ["1","2","3","0"]:
        return "error"
    record=User(name,sex,studentID,college,classs,qq,phoneNumber,department1,reason1,department2,reason2,interest,time,ip)
    db.session.add(record)
    db.session.commit()
    return "True"

if __name__=='__main__':
    db.create_all()
    # app.run()
    server = pywsgi.WSGIServer(('0.0.0.0', 12345), app)
    server.serve_forever()
