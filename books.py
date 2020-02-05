from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, exists
from sqlalchemy.orm import relationship
 

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/books_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='books'

db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = "authors"

    id = Column(Integer,primary_key=True)
    name = Column(String(16),unique=True)

    # 与Book 模型关联，反向映射的名字为authors ，这样查的时候就都写表名就行了
    books = relationship('Book', backref='authors')

    def __repr__(self):
        return 'Author: %s' % self.name


class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)
    author_id = Column(Integer,ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s' % (self.name,self.author_id)


@app.route('/aq', methods=['GET','POST'])
def aq():
    # 查询所有作者信息，传递给模板
    authors = Author.query.all()
    # authors = db.session.query(Author)
    if request.method == "POST":
        author = request.form.get("author")
        # 高级查询
        is_exist = db.session.query(exists().where(Author.name == author)).scalar()
        if is_exist:
            book = request.form.get("book")
            return render_template('books.html', authors=authors)
        else:
            return render_template('books.html', authors=authors,hint = '请检查作者是否注册')
    return render_template('books.html', authors=authors)


@app.route('/x', methods=['GET','POST'])
def index():
    # 查询所有作者信息，传递给模板
    authors = Author.query.all()
    # authors = db.session.query(Author)
    if request.method == "POST":
        author_form = request.form.get("author")
        book_form = request.form.get("book")
        author = Author.query.filter_by(name = author_form).first()  # 作者对象
        if author:
            # 如果作者存在
            book = Book.query.filter_by(name=book_form).first()
            if book:
                # 如果存在，提示重复
                return render_template('books.html', authors=authors, hint='已存在同名书籍')
            else:
                # 不存在就添加新书
                try:
                    new_book = Book(name=book_form, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    # 这里数据库一旦提交有问题，我们选择回滚
                    db.session.rollback()
                    return render_template('books.html', authors=authors, hint='添加书籍异常')
        else:
            # 如果作者不存在，先添加作者，再添加书籍
            try:
                new_author = Author(name=author_form)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_form, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template('books.html', authors=authors, hint='添加作者与书籍异常')

    authors = Author.query.all()
    return render_template('books.html', authors=authors)


@app.route('/del_book/<int:b_id>')
def del_book(b_id):
    book = Book.query.get(b_id)
    hint = None
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            hint = '删除异常'
            db.session.rollback()
    else:
        hint = '书未找到'
    return redirect(url_for('index',hint=hint))


@app.route('/del_author/<a_id>')
def del_author(a_id):
    # 先删书，再删作者
    author = Author.query.get(a_id)
    hint = None
    if author:
        try:
            # 查询之后直接删除
            Book.query.filter_by(author_id=author.id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            hint = '删除作者异常'
            db.session.roolback()
    else:
        hint = '作者未找到'
    return redirect(url_for('index', hint=hint))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    au1 = Author(name='小明')
    au2 = Author(name='小哈')
    au3 = Author(name='小红')
    db.session.add_all([au1,au2,au3])
    db.session.commit()

    bk1 = Book(name='Android 开发', author_id =au1.id)
    bk2 = Book(name='Python 开发', author_id =au1.id)
    bk3 = Book(name='mySQL 入门 ', author_id =au2.id)
    bk4 = Book(name='Flask 入门 ', author_id =au3.id)
    bk5 = Book(name='Flutter 入门 ', author_id =au3.id)
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    db.session.commit()

    app.run(debug=True)
