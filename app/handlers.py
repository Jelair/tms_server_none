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

from aiohttp import web
from coreweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError
from models import Test, next_id

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

@get('/api/test')
def api_test(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Test.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = yield from Test.findAll(orderBy='id desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)