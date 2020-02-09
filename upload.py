from flask_wtf import FlaskForm
from flask_wtf.csrf import validate_csrf
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import Flask, send_from_directory, render_template, flash, url_for, session, request
from werkzeug.utils import redirect
from wtforms import SubmitField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError
import os
import uuid

app = Flask(__name__)

app.secret_key = 'upload'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']


class UploadForm(FlaskForm):
    # FileRequired 验证是否包含文件对象
    # FileAllowed 用来验证文件类型，upload_set 来指定允许的文件后缀名列表
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/show_images')
def show_images():
    return render_template('show_images.html')


@app.route('/get_file/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


class MultiUploadForm(FlaskForm):
    image = MultipleFileField('Upload Image', validators={DataRequired()})
    submit = SubmitField()


@app.route('/multi_upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        # 验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))
        # 检查文件是否存在
        if 'image' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('image'):
            # 检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename ))
                filenames.append(filename)
            else:
                flash('Invalid file type:')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


if __name__ == '__main__':
    print("app.root_path:", app.root_path)
    app.run()





