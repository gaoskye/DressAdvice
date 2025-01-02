import os
from datetime import datetime

from flask import render_template, request
from flask import send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename

from run import app
from wxcloudrun.dao import *
from wxcloudrun.model import Counters
from wxcloudrun.recommend import recommend_clothes
from wxcloudrun.response import success_empty_response, success_response, err_response


@app.route('/api/clothes/add', methods=['POST'])
def add_clothes():
    try:
        # 获取请求体参数
        params = request.get_json()

        # 检查参数
        if 'user' not in params:
            return err_response('缺少user参数')
        if 'clothes' not in params:
            return err_response('缺少clothes参数')
        clothes_param = params['clothes']
        if 'name' not in clothes_param:
            return err_response('缺少name参数')
        if 'description' not in clothes_param:
            return err_response('缺少description参数')
        if 'category' not in clothes_param:
            return err_response('缺少category参数')
        if 'min_temp' not in clothes_param:
            return err_response('缺少min_temp参数')
        if 'max_temp' not in clothes_param:
            return err_response('缺少max_temp参数')
        if 'label' not in clothes_param:
            return err_response('缺少label参数')
        if 'image' not in clothes_param:
            return err_response('缺少image参数')

        user = params['user']
        name = clothes_param['name']
        description = clothes_param['description']
        category = clothes_param['category']
        min_temp = clothes_param['min_temp']
        max_temp = clothes_param['max_temp']
        label = clothes_param['label']
        image = clothes_param['image']

        # 校验字段类型
        if not isinstance(user, str):
            return err_response('user参数必须是字符串')
        if not isinstance(name, str):
            return err_response('name参数必须是字符串')
        if not isinstance(description, str):
            return err_response('description参数必须是字符串')
        if not isinstance(category, str):
            return err_response('category参数必须是字符串')
        if not isinstance(min_temp, int):
            return err_response('min_temp参数必须是整数')
        if not isinstance(max_temp, int):
            return err_response('max_temp参数必须是整数')
        if not isinstance(label, str):
            return err_response('label参数必须是字符串')
        if not isinstance(image, str):
            return err_response('image参数必须是字符串')

        # 插入衣服数据
        clothes = Clothes()
        clothes.user = user
        clothes.name = name
        clothes.description = description
        clothes.category = category
        clothes.min_temp = min_temp
        clothes.max_temp = max_temp
        clothes.label = label
        clothes.image = image

        insert_clothes(clothes)

        return success_response('衣服数据插入成功')

    except Exception as e:
        logger.error("insert_clothes errorMsg= {} ".format(e))
        return err_response(format(e))


@app.route('/api/clothes/query', methods=['GET'])
def query_clothes():
    try:
        # 从 URL 参数中获取参数
        user = request.args.get('user')
        cat = request.args.get('cat')
        min_temp = request.args.get('min_temp')
        max_temp = request.args.get('max_temp')

        if not user:
            return err_response('缺少user参数')

        if not cat and not min_temp and not max_temp:
            clothes = query_clothes_by_user(user)
        elif cat and not min_temp and not max_temp:
            clothes = query_clothes_by_user_cat(cat, user)
        elif not cat:
            return err_response('缺少cat参数')
        elif not min_temp:
            return err_response('缺少min_temp参数')
        elif not max_temp:
            return err_response('缺少max_temp参数')
        else:
            # 校验温度参数
            if not min_temp.isdigit() or not max_temp.isdigit():
                return err_response('温度参数必须是整数')

            min_temp = int(min_temp)
            max_temp = int(max_temp)

            if min_temp > max_temp:
                return err_response('min_temp不能大于max_temp')

            clothes = query_clothes_by_user_cat_temp(cat, min_temp, max_temp, user)

        return success_empty_response() if clothes is None else success_response(clothes)

    except Exception as e:
        logger.error("query_clothes errorMsg= {} ".format(e))
        return err_response(format(e))


@app.route('/api/clothes/recommend', methods=['GET'])
def recommend():
    try:
        # 从 URL 参数中获取参数
        city = request.args.get('city')
        user = request.args.get('user')
        weather_data, suitable_clothes, suitable_clothes_store = recommend_clothes(city, user)
        return success_response(
            {'weather': weather_data, 'clothesHave': suitable_clothes, 'clothesBrand': suitable_clothes_store})
    except Exception as e:
        logger.error("recommend_clothes errorMsg= {} ".format(e))
        return err_response(format(e))


@app.route('/api/clothes/advice', methods=['GET'])
def get_clothes_advice():
    try:
        # 从 URL 参数中获取参数
        location = request.args.get('location')
        return success_empty_response() if location is None else success_response(location)
    except Exception as e:
        logger.error("get_clothes_advice errorMsg= {} ".format(e))
        return err_response(format(e))


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
        return err_response('缺少action参数')

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
        return success_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return success_empty_response()

    # action参数错误
    else:
        return err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return success_response(0) if counter is None else success_response(counter.count)
