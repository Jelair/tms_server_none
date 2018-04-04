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

def test_users():
    r = requests.get('%suser' % base_url)
    rs = r.json()
    print(rs)
    return rs
#test_users()

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

def test_contract(userid):
    payload = {
        'userid': userid
    }
    r = requests.get('%scontract' % base_url, data=payload)
    print(r.json())
test_contract('001522851529077a38aa10ef322412ab71bb77b972447e1000')

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