from flask import Flask
from flask import render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/qflask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)

    users = relationship('User',backref='role')

    def __repr__(self):
        return '<Role: %s %s>' % (self.name,self.id)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)
    email = Column(String(32), unique=True)
    password = Column(String(32))
    role_id = Column(Integer,ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s %s %s %s>' % (self.name,self.id,self.email,self.password)


@app.route('/hello_world')
def hello_world():
    a = 10

    b = 2

    c = 2

    result = (a+b)/c
    
    return "<h1>雷浩</h1> %d" % result

@app.route('/hello')
def hello():
    # 我们用render_template来找到并处理我们的html 界面
    # 这样就会自动去找templates 文件夹的hello.html 文件
    return render_template("hello.html")

# 把一个变量发送到页面
@app.route('/arg')
def arg():
    s = "arg0"
    lst = ["狂战士","神思者","无极"]
    my_dict = {
        'name':'Sam',
        'age':18
    }
    return render_template("hello.html", jay = s,list = lst,my_dict = my_dict)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login',methods = ['post'])
def login():
    # 接收用户名与密码
    # 从请求里拿到数据，需要用到request
    # form 就可以立即为一个字典啦
    username = request.form.get("username")
    pwd = request.form.get("pwd")

    # url 传参这么可以接收
    # request.url.get()

    if username == "123" and pwd == "321":
        return "登录成功"
    else:
        return render_template("login.html",hint = "请检查用户名或密码")

@app.route('/orders/<int:id>')
def orders_id(id):
    return "order id %s" % id

@app.route('/orders')
def orders():
    return "请填编号"


if __name__ == '__main__':
    db.drop_all()

    db.create_all()

    ro1 = Role(name='admin')
    db.session.add(ro1)
    db.session.commit()

    ro2 = Role(name='user')
    db.session.add(ro2)
    db.session.commit()

    us1 = User(name='wang',email='w32353@163.com',password='123456',role_id=ro1.id)
    us2 = User(name='chen', email='chen@163.com', password='205522', role_id=ro1.id)
    us3 = User(name='zhou', email='2235368@qq.com', password='123336', role_id=ro1.id)
    us4 = User(name='tang', email='t32353@163.com', password='123qu6', role_id=ro1.id)
    us5 = User(name='wu', email='wu38353@163.com', password='123876', role_id=ro1.id)
    us6 = User(name='li', email='li39853@163.com', password='123407', role_id=ro1.id)
    us7 = User(name='feng', email='feng@163.com', password='123wda', role_id=ro1.id)
    us8 = User(name='wei', email='wei253@163.com', password='123002', role_id=ro1.id)
    us9 = User(name='liu', email='liu323@163.com', password='122456', role_id=ro1.id)
    us10 = User(name='yang', email='y32253@163.com', password='223206', role_id=ro1.id)
    db.session.add_all([us1,us2,us3,us4,us5,us6,us7,us8,us9,us10])
    db.session.commit()

    app.run(debug=True)
