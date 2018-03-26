#coding:utf-8
from django.shortcuts import render,HttpResponse
from models import *
import datetime
import json

import random,string

# Create your views here.
def index(request):
    return render(request, 'index.html')

#验证签名
'''
根据传的参数进行解密，判断签名是否正确
'''
def is_sign(request):
    flag = False
    # data = []
    # para = {}
    # if request.method == 'GET':
    #     para =request.GET.items()
    #     try:
    #         para.pop('username')
    #         para.pop('sign')
    #     except :
    #         print Exception
    #     else:
    #         for k,v in para.items():
    #             data.append(k+'='+v)
    #         data.sort()
    #         result = '&'.join(data)
    # elif request.method == 'POST':
    #     for k in request.POST:
    #         if k == 'username' or k == 'sing':
    #             continue
    #         else:
    #             para[k] = request.POST.get(k)
    #     for k,v in para.items():
    #         data.append(k+'='+v)
    #     data.sort()
    #     result = '&'.join(data)
    #     salt = ''.join(random.sample(string.ascii_letters + string.digits, 5))

    flag = True
    return flag


#系统管理员登录
def register(request):
    response = HttpResponse()

    return response

#添加会议
'''
校验内容：
1、校验请求类型
2、校验title、address、time，是否填写
3、校验title唯一
4、校验status值合法
5、校验签名正确

校验结果，按接口文档返回对应参数
数据操作：Event.object.create
'''
def add_event(request):
    # response = HttpResponse()
    error_code = '1'
    message = ''
    data = {}

    if request.method == 'POST':
        title = request.POST.get('title', None)
        limit = request.POST.get('limit', None)
        address = request.POST.get('address', None)
        status = request.POST.get('status', 0)
        time = request.POST.get('time', None)
        if title and address and time:
            try:
                Event.objects.get(title=title)
                error_code = '10002'
                message = u'title已存在'
            except Exception as e:
                print e
                try:
                    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    status = int(status)
                    limit = int(limit)
                    if status in (0, 1, 2):

                        if is_sign(request):
                            try:
                                event = Event.objects.create(title=title, limit=limit,
                                                    address=address, status=status, time=time)
                                error_code = '0'
                                data = {'event_id':event.id, 'status':event.status}
                                message = u'会议添加成功。'
                            except Exception as e:
                                print e
                                error_code = '10098' #数据操作异常
                                message = u'数据操作异常'

                        else:
                            error_code = '10011'
                            message = '签名错误'
                    else:
                        error_code = '10003'
                        message = u'签名错误'
                except Exception as e:
                    print e
                    error_code = '10098' #数据类型错误
                    message = u'数据类型错误'
        else:
            error_code = '10001'
            message = u'缺少必要参数'
    else:
        error_code = '10099' #请求类型错误
        message = u'请求类型错误'

    js = json.dumps({"error_code":error_code, 'data':data, "message":message})
    print js
    return HttpResponse(js)

#查询会议列表
'''
校验内容：
1、校验请求类型
2、根据title判断全查询，还是按标题模糊查询
3、查询列表为空，返回错误码10004
4、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：Event.object.filter,all
'''
def get_eventlist(request):

    error_code = '1'
    message = ''
    event_list = []
    if request.method == 'GET':
        if is_sign(request):
            title = request.GET.get('title', None)
            try:
                event_list = Event.objects.filter(title__contains=title).values('id', 'title', 'status')
                if event_list:
                    error_code = '0'
                    event_list = list(event_list)
                else:
                    event_list = list(event_list)
                    error_code = u'10004' # 未查询到会议信息
                    message = u'未查询到会议信息'

            except Exception as e:
                print e
                error_code = '10098' #数据操作异常
                message = u'数据操作异常'

        else:
            error_code = '10011'
            message = u'签名错误'

    else:
        error_code = '10099' #请求类型错误
        message = u'请求类型错误'

    js = json.dumps({'event_list':event_list, 'error_code': error_code, 'message': message})
    return HttpResponse(js)

#查询会议详细信息
'''
校验内容：
1、校验请求类型
2、校验id参数是否填写
3、根据id查找会议信息
4、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：Event.object.filter.value
'''
def get_eventdetail(request):
    response = HttpResponse()

    return response

#修改会议状态
'''
校验内容：
1、校验请求类型
2、校验id，status是否填写
3、判断status值是否合法
4、根据id查找会议信息
5、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：Event.object.update
'''
def set_status(request):
    response = HttpResponse()

    return response

#添加嘉宾
'''
校验内容：
1、校验请求类型
2、校验id、name、phone_number必填
3、根据id查找会议信息
4、id+phone_number确认嘉宾唯一
5、校验会议是否满员
6、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：Event.object.filter
          Guest.object.create
          Event.guest.add()
'''
def add_guest(request):
    response = HttpResponse()

    return response

#查询会议嘉宾
'''
校验内容：
1、校验请求类型
2、根据event_id查询会议信息
3、根据event_id+phone_number查询会议嘉宾信息
4、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：Guest.object.filter
          Event.object.value
'''
def get_guestlist(request):
    response = HttpResponse()

    return response

# 嘉宾签到
'''
校验内容：
1、校验请求类型
2、根据event_id+phone_number查询会议嘉宾信息是否匹配
3、校验是否已签到
4、校验会议是否结束
5、校验签名是否正确

校验结果，按接口文档返回对应参数
数据操作：原生sql
'''
def sign(request):
    response = HttpResponse()

    return response