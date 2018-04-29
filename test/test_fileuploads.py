# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_fileuploads
   Description :
   Author :       simplefly
   date：          2018/4/3
-------------------------------------------------
   Change Activity:
                   2018/4/3:
-------------------------------------------------
"""
__author__ = 'simplefly'

from aiohttp import web
import os
from app.coreweb import get, post, add_routes

@post('/upload')
async def store_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    # reader.next() will `yield` the fields of your form

    # field = await reader.next()
    # assert field.name == 'name'
    # name = await field.read(decode=True)

    field = await reader.next()
    #assert field.name == 'mp3'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    path = 'E:/upload/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

@get('/file/{filename}')
async def get_file(*, filename):
    print(filename)
    path = 'E:/upload/'
    with open(os.path.join(path, filename), 'rb') as f:
        data = f.read()
    return web.Response(body=data)

@get('/')
async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
add_routes(app, 'test_fileuploads')
web.run_app(app, host='127.0.0.1', port=8080)