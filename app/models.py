# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       simplefly
   date：          2018/3/19
-------------------------------------------------
   Change Activity:
                   2018/3/19:
-------------------------------------------------
"""
__author__ = 'simplefly'

import time, uuid
from orm import Model, StringField, BooleanField, FloatField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Test(Model):
    __table__ = 'test'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(255)')

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    username = StringField(ddl='varchar(32)')
    password = StringField(ddl='varchar(64)')
    nickname = StringField(ddl='varchar(64)')
    email = StringField(ddl='varchar(64)')
    sex = BooleanField()
    birthday = FloatField(default=time.time())
    phone = StringField(ddl='varchar(32)')
    token = StringField(ddl='varchar(255)')
    remark = StringField(ddl='varchar(255)')
    avatar = StringField(ddl='varchar(255)')
    create_date = FloatField(default=time.time())
    update_date = FloatField(default=time.time())

class File(Model):
    __table__ = 'files'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    filename = StringField(ddl='varchar(32)')
    filetype = StringField(ddl='varchar(10)')
    filesize = IntegerField()
    filepath = StringField(ddl='varchar(255)')
    userid = StringField(ddl='varchar(50)')
    upload_date = FloatField()

class Task(Model):
    __table__ = 'task'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    taskname = StringField(ddl='varchar(32)')
    taskcontent = StringField(ddl='varchar(255)')
    fileid = StringField(ddl='varchar(50)')
    deadline = FloatField()
    userid = StringField(ddl='varchar(50)')
    create_date = FloatField()
    level = IntegerField()
    parentid = StringField(ddl='varchar(50)')
    progress = IntegerField()

class Contract(Model):
    __table__ = 'contracts'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    userid = StringField(ddl='varchar(50)')
    contractid = StringField(ddl='varchar(50)')
    create_date = FloatField()
    note = StringField(ddl='varchar(50)')

class Member(Model):
    __table__ = 'member'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    taskid = StringField(ddl='varchar(50)')
    memberid = StringField(ddl='varchar(50)')
    create_date = FloatField()
    userid = StringField(ddl='varchar(50)')
    ismaster = BooleanField()

class Log(Model):
    __table__ = 'logs'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    taskid = StringField(ddl='varchar(50)')
    userid = StringField(ddl='varchar(50)')
    log_date = FloatField()
    logcontent = StringField(ddl='varchar(255)')

class Message(Model):
    __table__ = 'messages'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    fromuserid = StringField(ddl='varchar(50)')
    touserid = StringField(ddl='varchar(50)')
    send_date = FloatField()
    content = StringField(ddl='varchar(255)')