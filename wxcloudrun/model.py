from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Index

from wxcloudrun import db


class Clothes(db.Model):
    __tablename__ = 'clothes'
    __table_args__ = (
        Index('user_cat_temp', 'uid', 'category', 'min_temp', 'max_temp'),
    )

    id = Column(Integer, primary_key=True, comment='主键')
    name = Column(String(100), nullable=False, default='', comment='衣服名称')
    uid = Column(String(100), nullable=True, default='', comment='用户帐号')
    description = Column(String(500), nullable=True, default='', comment='衣服描述')
    category = Column(String(50), nullable=True, default='', comment='衣服分类')
    min_temp = Column(Integer, nullable=True, comment='适合最低温度')
    max_temp = Column(Integer, nullable=True, comment='适合最高温度')
    label = Column(String(100), nullable=True, default='', comment='衣服标签')
    image = Column(String(500), nullable=True, default='', comment='衣服图片')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class ClothesStore(db.Model):
    __tablename__ = 'clothes_store'
    __table_args__ = (
        Index('cat_temp', 'category', 'min_temp', 'max_temp'),
    )

    id = Column(Integer, primary_key=True, comment='主键')
    name = Column(String(100), nullable=False, default='', comment='衣服名称')
    description = Column(String(500), nullable=True, default='', comment='衣服描述')
    category = Column(String(50), nullable=True, default='', comment='衣服分类')
    min_temp = Column(Integer, nullable=True, comment='适合最低温度')
    max_temp = Column(Integer, nullable=True, comment='适合最高温度')
    label = Column(String(100), nullable=True, default='', comment='衣服标签')
    image = Column(String(500), nullable=True, default='', comment='衣服图片')
    link = Column(String(500), nullable=True, default='', comment='衣服链接')
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
