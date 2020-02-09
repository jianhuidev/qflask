from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/books_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='books'

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)

    users = relationship('User', backref='roles')

    # 帮助打印
    def __repr__(self):
        return '<Role: %s %s>' % (self.name,self.id)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s %s %s>' % (self.name,self.id,self.role_id)


@app.route('/')
def index():
    # print('***********')
    # print(User.query.get(1))
    # print(User.query.get(1).roles.name)
    # print('***********')
    # print('***********')
    # print(Role.query.get(2))
    # print(Role.query.get(2).users)
    # print(Role.query.get(2).users[0])
    # print(Role.query.get(2).users[0].name)
    # print('***********')
    return "12"


class LoginForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    pwd = PasswordField('密码：', validators=[DataRequired()])
    affirm_pwd = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('pwd', '密码不一致')])
    submit = SubmitField('提交')


@app.route('/form', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        affirm_pwd = request.form.get('affirm_pwd')

        print(username)
        print(pwd)
        print(affirm_pwd)
        # 验证参数
        # 需要加上CSRF token
        if login_form.validate_on_submit():
            return "成功"
        else:
            # print('请检查')
            flash('请检查')

    return render_template('index.html', form=login_form)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    role1 = Role(name='admin')
    role2 = Role(name='user')
    db.session.add_all([role1, role2])
    db.session.commit()
    user1 = User(name='小明', role_id=role1.id)
    user2 = User(name='小红', role_id=role2.id)
    user3 = User(name='小哈', role_id=role2.id)
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # print(role2)
    # print(user2)
    # print('******')
    # print(role2.users)
    # db.session.delete(role1)
    # db.session.commit()
    print("__file__:", __file__)
    print("app.root_path:", app.root_path)
    app.run(debug=True)
