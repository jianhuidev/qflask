from flask import request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import time
import os
import base64

app = Flask(__name__)
# UPLOAD_FOLDER = 'upload'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'upload'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = ['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF']


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload_api():
    return render_template('upload_api.html')


@app.route("/api/file/<filename>")
def file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


# 上传文件
@app.route('/api/upload', methods=['POST'])
def api_upload():
    # file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    file_dir = app.config['UPLOAD_PATH']
    # if not os.path.exists(file_dir):
    #     os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        # token = base64.b64encode(new_filename)
        # print(token)
        return jsonify({"code": 0, "msg": "ok", "token": 'a', "img_url": "http://127.0.0.1:5000/api/file/" + new_filename})
    else:
        return jsonify({"code": 1001, "msg": "no"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
