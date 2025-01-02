import os
from datetime import datetime

from flask import render_template, request
from flask import send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

from wxcloudrun.recommend import recommend_clothes
from run import app
from wxcloudrun.dao import *
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/api/clothes/add', methods=['POST'])
def add_clothes():
    # 获取请求体参数
    params = request.get_json()

    # 检查参数
    if 'name' not in params:
        return make_err_response('缺少name参数')
    if 'description' not in params:
        return make_err_response('缺少description参数')
    if 'category' not in params:
        return make_err_response('缺少category参数')
    if 'min_temp' not in params:
        return make_err_response('缺少min_temp参数')
    if 'max_temp' not in params:
        return make_err_response('缺少max_temp参数')
    if 'label' not in params:
        return make_err_response('缺少label参数')
    if 'image' not in params:
        return make_err_response('缺少image参数')

    name = params['name']
    description = params['description']
    category = params['category']
    min_temp = params['min_temp']
    max_temp = params['max_temp']
    label = params['label']
    image = params['image']

    # 校验字段类型
    if not isinstance(name, str):
        return make_err_response('name参数必须是字符串')
    if not isinstance(description, str):
        return make_err_response('description参数必须是字符串')
    if not isinstance(category, str):
        return make_err_response('category参数必须是字符串')
    if not isinstance(min_temp, int):
        return make_err_response('min_temp参数必须是整数')
    if not isinstance(max_temp, int):
        return make_err_response('max_temp参数必须是整数')
    if not isinstance(label, str):
        return make_err_response('label参数必须是字符串')
    if not isinstance(image, str):
        return make_err_response('image参数必须是字符串')

    # 插入衣服数据
    insert_clothes(params)

    return make_succ_response('衣服数据插入成功')


@app.route('/api/clothes/query', methods=['GET'])
def query_clothes():
    # 从 URL 参数中获取参数
    cat = request.args.get('cat')
    min_temp = request.args.get('min_temp')
    max_temp = request.args.get('max_temp')

    # 检查参数
    if not cat:
        return make_err_response('缺少cat参数')

    if not min_temp and not max_temp:
        clothes = query_clothes_by_cat(cat)
    elif not min_temp:
        return make_err_response('缺少min_temp参数')
    elif not max_temp:
        return make_err_response('缺少max_temp参数')
    else:
        # 校验温度参数
        if not min_temp.isdigit() or not max_temp.isdigit():
            return make_err_response('温度参数必须是整数')

        min_temp = int(min_temp)
        max_temp = int(max_temp)

        if min_temp > max_temp:
            return make_err_response('min_temp不能大于max_temp')

        clothes = query_clothes_by_cat_temp(cat, min_temp, max_temp)

    return make_succ_empty_response() if clothes is None else make_succ_response(clothes)


@app.route('/api/clothes/recommend', methods=['GET'])
def recommend_clothes():
    # 从 URL 参数中获取参数
    location = request.args.get('location')
    weather_data, suitable_clothes, suitable_clothes_store = recommend_clothes(location)
    return make_succ_response({'weather': weather_data, 'clothesHave': suitable_clothes, 'clothesBrand': suitable_clothes_store})


@app.route('/api/clothes/advice', methods=['GET'])
def get_clothes_advice():
    # 从 URL 参数中获取参数
    location = request.args.get('location')
    return make_succ_empty_response() if location is None else make_succ_response(location)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/clothes/image', methods=['GET', 'POST'])
def upload_clothes_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
