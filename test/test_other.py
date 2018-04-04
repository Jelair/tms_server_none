# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_other
   Description :
   Author :       simplefly
   date：          2018/4/2
-------------------------------------------------
   Change Activity:
                   2018/4/2:
-------------------------------------------------
"""
__author__ = 'simplefly'

import json

l = [{'id': '00152265144038712d2a0886a4d4477a5b8013f51022415000', 'username': 'admin', 'password': '0c663e8c12b5e39788d78bf4193550ba7342c789', 'nickname': 'admin', 'email': '2478151585@qq.com', 'sex': 0, 'phone': '18835231839', 'token': '432', 'remark': '432', 'avatar': '432', 'create_date': 1522651392.32758, 'update_date': 1522651392.32758}]
l2 = [{'id': '00152265144038712d2a0886a4d4477a5b8013f51022415000',
       'username': 'admin'}]
s = json.dumps(l, ensure_ascii=False, default=lambda o:o.__dict)
print(s)