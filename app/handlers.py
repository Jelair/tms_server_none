# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     handlers
   Description :
   Author :       simplefly
   date：          2018/3/19
-------------------------------------------------
   Change Activity:
                   2018/3/19:
-------------------------------------------------
"""
__author__ = 'simplefly'
import re, time, json, logging, hashlib, base64, asyncio
from aiohttp import web
from coreweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError
from models import Test, next_id, User, File, Member, Message, Task, Log, Contract
from utils.rongcloud_utils import get_token

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

@get('/api/user')
def api_user(*, page='1'):
    page_index = get_page_index(page)
    num = yield from User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = yield from User.findAll(limit=(p.offset, p.limit))
    print(users)
    return dict(page=p, users=users)

@get('/api/user/checkusername')
def api_check_username(*, username):
    if not username:
        raise APIValueError('username', 'Invalid username.')
    users = yield from User.findAll('username=?', [username])
    return {
        'check' :username,
        'count' :len(users)
    }

@get('/api/user/checkemail')
def api_check_email(*, email):
    if not email:
        raise APIValueError('email', 'Invalid email')
    users = yield from User.findAll('email=?', [email])
    return {
        'check' :email,
        'count' :len(users)
    }

@get('/api/user/checkphone')
def api_check_phone(*, phone):
    if not phone:
        raise APIValueError('phone', 'Invalid phone')
    users = yield from User.findAll('phone=?', [phone])
    return {
        'check' :phone,
        'count' :len(users)
    }

@post('/api/user/register')
def api_user_register(*, email, phone, username, password):
    if not email or not email.strip():
        raise APIValueError('email')
    if not phone or not phone.strip():
        raise APIValueError('phone')
    if not username or not username.strip():
        raise APIValueError('username')
    if not password or not password.strip():
        raise APIValueError('password')
    uid = next_id()
    try:
        result = yield from get_token(uid)
        token = result['token']
    except Exception as e:
        logging.info(e)

    sha1_passwd = '%s:%s' % (uid, password)
    spwd = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()
    user = User(id=uid, username=username.strip(), nickname=username.strip(), email=email, password=spwd, phone=phone, token=token)
    result = yield from user.save()
    return {
        'result' : result,
        'token' : token
    }

@get('/api/contract')
def api_contract(*, userid, page='1'):
    page_index = get_page_index(page)
    num = yield from Contract.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, contract=())
    sql = 'SELECT `users`.id,`users`.username,`users`.nickname,`users`.email,`users`.birthday,`users`.sex,`users`.avatar,' \
          '`users`.phone,`users`.remark,users.create_date,users.update_date,contracts.create_date AS contract_date,contracts.note ' \
          'FROM users LEFT JOIN contracts ON users.id = contracts.contractid WHERE users.id in (SELECT contractid FROM ' \
          'contracts WHERE `contracts`.userid = ?);'
    contracts = yield from Contract.mselect(sql, [userid])
    print(contracts)
    return dict(page=p, contract=contracts)

@post('/api/contract/new')
def api_contract_new(*, userid, contractid):
    if not userid:
        raise APIValueError('userid')
    if not contractid:
        raise APIValueError('contractid')
    fromid = next_id()
    fcontract = Contract(id=fromid, userid=userid, contractid=contractid)
    fres = yield from fcontract.save()
    toid = next_id()
    tcontract = Contract(id=toid, userid=contractid, contractid=userid)
    tres = yield from tcontract.save()
    return {
        'fres' : fres,
        'tres' : tres
    }
