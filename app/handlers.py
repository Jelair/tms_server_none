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
import re, time, json, logging, hashlib, base64, asyncio, os
from aiohttp import web
from coreweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError
from models import next_id, User, File, Member, Message, Task, Log, Contract, TaskResult, RemindMsg
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

@post('/api/upload')
def api_upload(request):
    reader = yield from request.multipart()
    field = yield from reader.next()
    filename = field.filename
    size = 0
    path = 'E:/upload/'
    id = next_id()
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, filename), 'wb') as f:
        while True:
            chunk = yield from field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    file = File(id=id, filename=filename, filepath=filename, filesize=size)
    affected = yield from file.save()
    return {
        'affected': affected
    }

@get('/api/file/{filename}')
def api_download(*, filename):
    path = 'E:/upload/'
    with open(os.path.join(path, filename), 'rb') as f:
        data = f.read()
    return data

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

    #sha1_passwd = '%s:%s' % (uid, password)
    #spwd = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()
    user = User(id=uid, username=username.strip(), nickname=username.strip(), email=email, password=password, phone=phone, token=token)
    result = yield from user.save()
    return {
        'result' : result
    }

@get('/api/user/login')
def api_user_login(*, username=None, email=None, phone=None, password=None):
    'check login information'
    if not username or not username.strip():
        if not email or not email.strip():
            if not phone or not phone.strip():
                print(username, email, phone, password)
                return dict(user=())
            else:
                user = yield from User.findAll('phone=? and password=?', [phone, password])
        else:
            user = yield from User.findALL('email=? and password=?', [email, password])
    else:
        user = yield from User.findAll('username=? and password=?', [username, password])
    return dict(user=user)

@get('/api/user/info')
def api_user_info(*, userid):
    'search person and get persanal infomation'
    if not userid:
        raise APIValueError('userid')
    user = yield from User.findAll('id=?', [userid])
    return dict(user=user)

@post('/api/user/update')
def api_user_update(*, userid):
    pass

@get('/api/contract')
def api_contract(*, userid, page='1'):
    'get person contract'
    print(userid)
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

@get('/api/contract/check')
def api_contract_check(*, userid, contractid):
    if not userid:
        raise APIValueError('userid')
    if not contractid:
        raise APIValueError('contractid')
    contracts = yield from Contract.findAll('userid=? AND contractid=?',[userid, contractid])
    return {
        'count': len(contracts)
    }

@post('/api/contract/new')
def api_contract_new(*, userid, contractid):
    'add contract'
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

@get('/api/contract/search')
def api_contract_search(*, username=None, phone=None, email=None):
    if not username or not username.strip():
        if not email or not email.strip():
            if not phone or not phone.strip():
                return dict(user=())
            else:
                user = yield from User.findAll('phone=?', [phone])
        else:
            user = yield from User.findAll('email=?', [email])
    else:
        user = yield from User.findAll('username=?', [username])
    return dict(user=user)

@post('/api/msg/apply')
def api_contract_apply(*, fromuserid, touserid, taskid=None, content):
    if not fromuserid:
        raise APIValueError('fromuserid')
    if not touserid:
        raise APIValueError('touserid')
    id = next_id()
    msg = Message(id=id, fromuserid=fromuserid, touserid=touserid, taskid=taskid, content=content)
    res = yield from msg.save()
    return {
        'res': res
    }

@get('/api/msg/list')
def api_msg_list(*, userid):
    if not userid:
        raise APIValueError('userid')
    msgs = yield from Message.mselect('SELECT messages.id, messages.fromuserid,messages.taskid, messages.send_date, messages.content, users.username FROM messages LEFT JOIN users ON messages.fromuserid = users.id WHERE messages.isovertime = FALSE AND messages.touserid = ?;', [userid])
    return dict(message=msgs)

@get('/api/msg/task/list')
def api_msg_task_list(*, userid):
    if not userid:
        raise APIValueError('userid')
    msgs = yield from Message.mselect('SELECT messages.id, messages.taskid, messages.fromuserid, messages.send_date, messages.content, users.username FROM messages LEFT JOIN users ON messages.fromuserid = users.id WHERE messages.taskid IS not NULL AND messages.touserid = ?;', [userid])
    return dict(message=msgs)

@post('/api/msg/overtime')
def api_msg_overtime(*, msgid):
    if not msgid:
        raise APIValueError('msgid')
    affected = yield from Message.mexecute('UPDATE messages SET isovertime = TRUE WHERE id = ?', [msgid])
    return {
        'affected': affected
    }

@post('/api/contract/delete')
def api_contract_delete(*, userid, contractid):
    'delete contract'
    if not userid:
        raise APIValueError('userid')
    if not contractid:
        raise  APIValueError('contractid')
    affected = yield from Contract.mexecute('DELETE FROM contracts WHERE userid=? and contractid=?', [userid, contractid])
    affected2 = yield from Contract.mexecute('DELETE FROM contracts WHERE userid=? and contractid=?',
                                            [contractid, userid])
    return {
        'affected': affected,
        'affected2': affected2
    }

@post('/api/contract/update')
def api_contract_update(*, userid, contractid, note):
    'add note for contract'
    if not userid:
        raise APIValueError('userid')
    if not contractid:
        raise APIValueError('contractid')
    affected = yield from Contract.mexecute('UPDATE contracts SET note = ? WHERE userid = ? AND contractid = ?;',[note,userid,contractid])
    return {
        'affected': affected
    }

@post('/api/task/new')
def api_task_new(*, userid, taskname, taskcontent, fileid=None, deadline, parentid=None):
    'new task and record in log'
    if not userid:
        raise APIValueError('userid')
    if not taskname or not taskname.strip():
        raise APIValueError('taskname')
    if not taskcontent or not taskcontent.strip():
        raise APIValueError('taskcontent')
    id = next_id()
    task = Task(id=id, userid=userid, taskname=taskname, taskcontent=taskcontent, deadline=deadline, fileid=fileid, parentid=parentid)
    affected = yield from task.save()
    id2 = next_id()
    logstr = '创建了任务（%s）' % taskname
    log = Log(id=id2, userid=userid, taskid=id, logcontent=logstr)
    affected2 = yield from log.save()
    id3 = next_id()
    member = Member(id=id3, taskid=id, memberid=userid, userid=userid, ismaster=True)
    affected3 = yield from member.save()
    if parentid:
        id4 = next_id()
        childlogstr = '创建了子任务（%s）' % taskname
        log = Log(id=id4, userid=userid, taskid=parentid, logcontent=childlogstr)
        yield from log.save()
    return {
        'affected': affected,
        'logaffected': affected2,
        'memaffected': affected3
    }

@get('/api/task/list')
def api_task_list(*, userid):
    if not userid:
        raise APIValueError('userid')
    nowtime = time.time()
    tasks = yield from Task.mselect('SELECT taskid, taskname, taskcontent, fileid, deadline, task.create_date AS create_date, '
                         'parentid, progress, memberid, ismaster FROM task LEFT JOIN member ON task.id = member.taskid '
                         'WHERE member.memberid = ? AND progress < 100 AND deadline > ? AND task.parentid IS NULL;', [userid, nowtime])
    return dict(tasks=tasks)

@get('/api/task/historylist')
def api_task_historylist(*, userid):
    if not userid:
        raise APIValueError('userid')
    nowtime = time.time()
    tasks = yield from Task.mselect('SELECT taskid, taskname, taskcontent, fileid, deadline, task.create_date AS create_date, '
                         'parentid, progress, memberid, ismaster FROM task LEFT JOIN member ON task.id = member.taskid '
                         'WHERE member.memberid = ? AND (progress = 100 OR deadline <= ?) ORDER BY deadline DESC;', [userid, nowtime])
    return dict(historytasks=tasks)

@get('/api/task/member')
def api_task_member(*, taskid):
    if not taskid:
        raise APIValueError('taskid')
    member = yield from Member.mselect('SELECT users.id, users.avatar, users.birthday, users.create_date, users.email, '
                                       'users.nickname, users.phone, users.remark, users.sex, users.username, member.ismaster FROM users '
                                       'LEFT JOIN member ON users.id = memberid WHERE taskid = ?;', [taskid])
    return dict(member=member)

@post('/api/task/member/invite')
def api_task_member_invite(*, taskid, memberid, userid, username):
    if not taskid:
        raise APIValueError('taskid')
    if not memberid:
        raise APIValueError('memberid')
    if not userid:
        raise APIValueError('userid')
    id = next_id()
    member = Member(id=id, taskid=taskid, memberid=memberid, userid=userid, ismaster=False)
    affected = yield from member.save()
    id2 = next_id()
    logstr = '邀请了新成员（%s）' % username
    log = Log(id=id2, userid=userid, taskid=id, logcontent=logstr)
    affected2 = yield from log.save()
    return {
        'affected': affected,
        'affected2': affected2
    }

@get('/api/task/log')
def api_task_log(*, taskid):
    if not taskid:
        raise APIValueError('taskid')
    log = yield from Log.mselect('SELECT `logs`.id, `logs`.logcontent, `logs`.log_date, users.username FROM `logs` '
                                 'LEFT JOIN users ON `logs`.userid = users.id WHERE `logs`.taskid = ? ORDER BY log_date DESC ;', [taskid])
    return dict(log=log)

@get('/api/task/childtask')
def api_task_childtask(*, taskid):
    if not taskid:
        raise APIValueError('taskid')
    childtask = yield from Task.findAll('parentid=?', [taskid], orderBy='create_date desc')
    return dict(childtask=childtask)

@post('/api/task/submit')
def api_task_submit(*, taskid, userid, fileid=None, desc=None, progress):
    if not taskid:
        raise APIValueError('taskid')
    if not userid:
        raise APIValueError('userid')
    id = next_id()
    taskresult = TaskResult(id=id, taskid=taskid, userid=userid, fileid=fileid, desc=desc)
    affected = yield from taskresult.save()
    id2 = next_id()
    logstr = '提交了任务'
    log = Log(id=id2, userid=userid, taskid=taskid, logcontent=logstr)
    affected2 = yield from log.save()
    affected3 = yield from Task.mexecute('UPDATE task SET progress = ? WHERE id = ?;', [progress, taskid])
    return {
        'affected': affected,
        'logaffected': affected2,
        'taskaffected': affected3
    }

@get('/api/task/result')
def api_task_result(*, taskid):
    if not taskid:
        raise APIValueError('taskid')
    taskresult = yield from TaskResult.mselect('SELECT taskresult.id, taskresult.fileid, taskresult.`desc`, '
                                               'taskresult.submit_date, users.username FROM taskresult LEFT JOIN '
                                               'users ON taskresult.userid = users.id WHERE taskresult.taskid = ?;', [taskid])
    return dict(taskresult=taskresult)

@post('/api/msg/remind')
def api_msg_remind(*, fromuserid, touserid, content):
    if not fromuserid:
        raise APIValueError('fromuserid')
    if not touserid:
        raise APIValueError('touserid')
    id = next_id()
    remindmsg = RemindMsg(id=id, fromuserid=fromuserid, touserid=touserid, content=content)
    affected = yield from remindmsg.save()
    return {
        'affected': affected
    }

@post('/api/msg/remind/overtime')
def api_msg_remind_overtime(*, remindmsgid):
    if not remindmsgid:
        raise APIValueError('remindmsgid')
    affected = yield from RemindMsg.mexecute('UPDATE remindmsg SET isovertime = TRUE WHERE id = ?', [remindmsgid])
    return {
        'affected': affected
    }

@get('/api/msg/remind/list')
def api_msg_remind_list(*, userid):
    if not userid:
        raise APIValueError('userid')
    remindmsg = yield from RemindMsg.findAll('touserid=? AND isovertime=False', [userid])
    return dict(remindmsg=remindmsg)

@post('/api/log/new')
def api_log_new(*, userid, taskid, logcontent):
    'new log'
    if not userid:
        raise APIValueError('userid')
    if not taskid:
        raise APIValueError('taskid')
    id = next_id()
    log = Log(id=id, userid=userid, taskid=taskid, logcontent=logcontent)
    affected = yield from log.save()
    return {
        'affected': affected
    }

@get('/api/log')
def api_log(*, taskid):
    'get log infomation'
    if not taskid:
        raise APIValueError('taskid')
    logs = yield from Log.mselect('SELECT users.username, `logs`.log_date, `logs`.logcontent FROM `logs` '
                                  'LEFT JOIN users ON `logs`.userid = users.id WHERE taskid = ? ORDER BY log_date desc;', [taskid])
    return dict(logs=logs)

@get('/api/statistical')
def api_statistical(*, userid, indays=30):
    if not userid:
        raise APIValueError('userid')
    # 先查询出近期indays内自己所参与的任务
    now = time.time()
    timeagostramp = now - indays * 3600 * 24
    tasks = yield from Member.findAll('memberid=? AND create_date>=?', [userid, timeagostramp])
    memberids = set()
    for task in tasks:
        # 根据taskid找出memberid
        members = yield from Member.findAll('taskid=?', [task['taskid']])
        for member in members:
            memberids.add(member['memberid'])
    rs = list()
    maxnum = 0
    for memberid in memberids:
        temp = dict()
        temp['userid'] = memberid
        user = yield from User.findAll('id=?', [memberid])
        temp['username'] = user[0]['username']
        snum = yield from Task.mselect('SELECT task.id FROM task LEFT JOIN member ON task.id = member.taskid '
                         'WHERE member.memberid = ? AND progress = 100 AND deadline > ?;', [memberid, timeagostramp])
        s_num = len(snum)
        temp['successnum'] = s_num
        fnum = yield from Task.mselect('SELECT task.id FROM task LEFT JOIN member ON task.id = member.taskid '
                         'WHERE member.memberid = ? AND progress < 100 AND deadline <= ? AND deadline > ?;', [memberid, now, timeagostramp])
        f_num = len(fnum)
        temp['failednum'] = f_num
        dnum = yield from Task.mselect('SELECT task.id FROM task LEFT JOIN member ON task.id = member.taskid '
                         'WHERE member.memberid = ? AND progress < 100 AND deadline > ?;', [memberid, now])
        d_num = len(dnum)
        temp['donum'] = d_num
        if s_num > maxnum:
            maxnum = s_num
        if f_num > maxnum:
            maxnum = f_num
        if d_num > maxnum:
            maxnum = d_num
        rs.append(temp)

    startard = 10
    while maxnum >= startard:
        startard += 10

    return dict(result=rs, startard=startard)

@get('/api/msg/count')
def api_msg_count(*, userid):
    if not userid:
        raise APIValueError('userid')
    newmsgs = yield from Message.findAll('isovertime=False AND touserid=?', [userid])
    remindmsgs = yield from RemindMsg.findAll('isovertime=False AND touserid=?', [userid])
    return {
        'newmsgs': len(newmsgs),
        'remindmsgs': len(remindmsgs)
    }