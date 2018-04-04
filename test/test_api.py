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

def test():
    r = requests.get('%stest' % base_url)
    print(r.json())

def test_users():
    r = requests.get('%suser' % base_url)
    print(r.json())
test_users()

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