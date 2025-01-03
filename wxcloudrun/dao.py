import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.model import Clothes, ClothesStore
from wxcloudrun.model import Counters

# 初始化日志
logger = logging.getLogger('log')


def insert_clothes(clothes: Clothes):
    """
    插入一个clothes实体
    :param clothes: Clothes实体
    """
    try:
        db.session.add(clothes)
        db.session.commit()
    except OperationalError as e:
        logger.error("insert_clothes errorMsg= {} ".format(e))
        raise e


def query_clothes_by_user(user):
    """
    根据分类查询clothes
    :param user: 用户账号
    :param cat: 分类
    :return: Clothes实体
    """
    try:
        return Clothes.query.filter(Clothes.uid == user).all()
    except OperationalError as e:
        logger.error("query_clothes_by_user errorMsg= {} ".format(e))
        raise e


def query_clothes_by_user_cat(cat, user):
    """
    根据分类查询clothes
    :param user: 用户账号
    :param cat: 分类
    :return: Clothes实体
    """
    try:
        return Clothes.query.filter(Clothes.uid == user, Clothes.category == cat).all()
    except OperationalError as e:
        logger.error("query_clothes_by_user_cat errorMsg= {} ".format(e))
        raise e


def query_clothes_by_user_cat_temp(cat, min_temp, max_temp, user):
    """
    根据分类和温度查询clothes
    :param user: 用户账号
    :param cat: 分类
    :param min_temp: 最低温度
    :param max_temp: 最高温度
    :return: Clothes实体
    """
    if min_temp > max_temp:
        raise ValueError('min_temp不能大于max_temp')
    try:
        return Clothes.query.filter(Clothes.uid == user, Clothes.category == cat, Clothes.min_temp <= min_temp,
                                    Clothes.max_temp >= max_temp).all()
    except OperationalError as e:
        logger.error("query_clothes_by_user_cat_temp errorMsg= {} ".format(e))
        raise e


def insert_clothes_store(clothes_store: ClothesStore):
    """
    插入一个clothes_store实体
    :param clothes_store: ClothesStore实体
    """
    try:
        db.session.add(clothes_store)
        db.session.commit()
    except OperationalError as e:
        logger.error("insert_clothes_store errorMsg= {} ".format(e))
        raise e


def query_clothes_store_by_cat(cat):
    """
    根据分类查询clothes_store
    :param cat: 分类
    :return: Clothes实体
    """
    try:
        return ClothesStore.query.filter(ClothesStore.category == cat).all()
    except OperationalError as e:
        logger.error("query_clothes_store_by_cat errorMsg= {} ".format(e))
        raise e


def query_clothes_store_by_cat_temp(cat, min_temp, max_temp):
    """
    根据分类和温度查询clothes_store
    :param cat: 分类
    :param min_temp: 最低温度
    :param max_temp: 最高温度
    :return: Clothes实体
    """
    if min_temp > max_temp:
        raise ValueError('min_temp不能大于max_temp')
    try:
        return ClothesStore.query.filter(ClothesStore.category == cat, ClothesStore.min_temp <= min_temp,
                                         ClothesStore.max_temp >= max_temp).all()
    except OperationalError as e:
        logger.error("query_clothes_store_by_cat_temp errorMsg= {} ".format(e))
        raise e


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))
