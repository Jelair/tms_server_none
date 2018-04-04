# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_rongcloud
   Description :
   Author :       simplefly
   date：          2018/4/3
-------------------------------------------------
   Change Activity:
                   2018/4/3:
-------------------------------------------------
"""
__author__ = 'simplefly'

from utils.rongcloud_utils import get_token

r = get_token('123456')
print(type(r), r)