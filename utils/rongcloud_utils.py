# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     rongcloud_utils
   Description :
   Author :       simplefly
   date：          2018/4/3
-------------------------------------------------
   Change Activity:
                   2018/4/3:
-------------------------------------------------
"""
__author__ = 'simplefly'

from rongcloud import RongCloud
import asyncio

app_key = '8luwapkv8r80l'
app_secret = '57ldbPu5Uzk'
rcloud = RongCloud(app_key, app_secret)

@asyncio.coroutine
def get_token(userId, name='username', portraitUri='http://www.rongcloud.cn/images/logo.png'):
    '''
    return token by userid
    :param userId:
    :param name:
    :param portraitUri:
    :return: dict
    '''
    r = rcloud.User.getToken(userId=userId, name=name, portraitUri=portraitUri)
    return r.result