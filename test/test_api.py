# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_api
   Description :
   Author :       simplefly
   date：          2018/4/2
-------------------------------------------------
   Change Activity:
                   2018/4/2:
-------------------------------------------------
"""
__author__ = 'simplefly'

import requests
base_url = 'http://127.0.0.1:8000/api/'
remo_url = 'http://119.3.29.176:8000/api/'

def test_users():
    r = requests.get('%suser' % remo_url)
    rs = r.json()
    print(rs)
    return rs
#test_users()

def test_task_st(userid):
    payload = {'userid': userid}
    r = requests.get('%sstatistical' % base_url, params=payload)
    print(r.json())
test_task_st('0015247910663195a94786ca59f4c4d888212c69cc7a1d8000')

def test_check_username(username):
    payload = {'username': username}
    r = requests.get('%suser/checkusername' % base_url, params=payload)
    print(r.json())
#test_check_username('admin')

def test_check_email(email):
    payload = {'email': email}
    r = requests.get('%suser/checkemail' % base_url, params=payload)
    print(r.json())
#test_check_email('2478151585@qq.com')

def test_check_phone(phone):
    payload = {'phone': phone}
    r = requests.get('%suser/checkphone' % base_url, params=payload)
    print(r.json())
#test_check_phone('18835231839')

def test_register(email, phone, username, password):
    payload = {
        'email': email,
        'phone': phone,
        'username': username,
        'password': password
    }
    r = requests.post('%suser/register' % base_url, data=payload)
    print(r.json())
#test_register('2478151585@qq.com', '18835231839', 'admin', '123456')

def test_contract_new(userid, contractid):
    payload = {
        'userid': userid,
        'contractid': contractid
    }
    r = requests.post('%scontract/new' % base_url, data=payload)
    print(r.json())

def test_contract_delete(userid, contractid):
    payload = {
        'userid': userid,
        'contractid': contractid
    }
    r = requests.post('%scontract/delete' % base_url, data=payload)
    print(r.json())
#test_contract_delete('001522851529077a38aa10ef322412ab71bb77b972447e1000', '0015228515296709c90c69101fa4102875a55eda1a0bb5f000')

def test_contract(userid):
    payload = {
        'userid': userid
    }
    r = requests.get('%scontract' % base_url, params=payload)
    print(r.json())
#test_contract('001522851529077a38aa10ef322412ab71bb77b972447e1000')

def action_add_users(count):
    import random
    for i in range(count):
        num = random.randint(10000, 1000000)
        email = '%d@qq.com' % num
        phone = str(num)
        rand_range = random.randint(3, 10)
        rand_list = random.sample(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z'], rand_range)
        username = ''.join(rand_list)
        password = '******'
        test_register(email, phone, username, password)
#action_add_users(10)

def action_add_contracts(userid):
    rs = test_users()
    rs = rs['users']
    for r in rs:
        if r['id'] == userid:
            continue
        test_contract_new(userid, r['id'])
#action_add_contracts('001522851529077a38aa10ef322412ab71bb77b972447e1000')

def test_login(*, username, email, phone, password):
    payload = {
        'phone': phone,
        'password': password
    }
    r = requests.get('%suser/login' % base_url, params=payload)
    print(r.json())

    payload2 = {
        'username': username,
        'password': password
    }
    r2 = requests.get('%suser/login' % base_url, params=payload2)
    print(r2.json())

    payload3 = {
        'email': email,
        'password': password
    }
    r3 = requests.get('%suser/login' % base_url, params=payload3)
    print(r3.json())

#test_login(username='nhi', email='146054@qq.com', phone='14654', password='9c35d41622b8a3910141f91fce255d8befe38f36')

def test_info(userid):
    payload = {
        'userid': userid
    }
    r = requests.get('%suser/info' % base_url, params=payload)
    print(r.json())
#test_info('001522851529077a38aa10ef322412ab71bb77b972447e1000')

def test_contract_update(note, userid, contractid):
    payload = {
        'note': note,
        'userid':  userid,
        'contractid': contractid
    }
    r = requests.post('%scontract/update' % base_url, data=payload)
    print(r.json())
#test_contract_update('aaa', '0015228515296709c90c69101fa4102875a55eda1a0bb5f000', '001522851529077a38aa10ef322412ab71bb77b972447e1000')

def test_task_new(userid, taskname, taskcontent, deadline):
    payload = {
        'userid': userid,
        'taskname': taskname,
        'taskcontent': taskcontent,
        'deadline': deadline,
    }
    r = requests.post('%stask/new' % base_url, data=payload)
    r = r.json()
    print(r)
#test_task_new('0015228515296709c90c69101fa4102875a55eda1a0bb5f000', 'run', 'runing', 132131)

def test_log(taskid):
    payload = {
        'taskid': taskid
    }
    rs = requests.get('%slog' % base_url, params=payload)
    print(rs.json())
#test_log('1')

def test_task_list(id):
    payload = {
        'userid': id
    }
    rs = requests.get('%stask/list' % base_url, params=payload)
    print(rs.json())
#test_task_list('1')
