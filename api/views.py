#coding:utf-8
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from models import *
from rest_framework.decorators import api_view
import datetime
import json
import base64
from django.contrib import auth
from rest_framework.authtoken.models import Token
import hashlib
from django.contrib.auth.models import *
# Create your views here.

def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def index(request):
    return render(request, 'index.html')

#验证签名
'''
根据传的参数进行解密，判断签名是否正确
'''

def is_sign(request):
    flag = False
    random = request.META.get('HTTP_RANDOM', None)
    token = request.META.get('HTTP_TOKEN', None)
    if request.method== "POST":
        username = request.POST.get('username')
    else:
        username = request.GET.get('username')
    user = User.objects.filter(username=username).first()
    server_token = Token.objects.get(user=user).key
    data = []
    para = {}
    if token == server_token:
        if request.method == 'GET':
            sign = request.GET.get('sign')
            keys =request.GET.keys()
            print keys
            for k in keys:
                if k == 'username' or k == 'sign':
                    continue
                else:
                    data.append(k+'='+request.GET.get(k))
                data.sort()
                result = '&'.join(data)
        else:
            sign = request.POST.get('sign')
            for k in request.POST.keys():
                # if k == 'username' or k == 'sing':
                #     continue
                # else:
                #     para[k] = request.POST.get(k)
            # for k,v in para.items():
                if k == 'username' or k == 'sign':
                    continue
                else:
                    v = request.POST.get(k)
                    data.append(k+'='+v)
            data.sort()
            result = '&'.join(data)

        sign_str = token+'para='+result+random
        print sign_str
        md5 = hashlib.md5()
        md5.update(sign_str.encode(encoding="utf-8"))
        server_sign = md5.hexdigest()
        print server_sign
        if sign == server_sign:
            flag = True
    return flag


#系统管理员登录
@api_view(['POST'],)
def register(request):
    error_code = ''
    token = ''
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if username and password:
        password = base64.decodestring(password)[3:]
        user = auth.authenticate(username=username, password=password)
        if user:
            token = Token.objects.get(user=user).key
            error_code = '0'
        else:
            error_code = '10000'
    else:
        error_code = '10001'

    js = {"error_code":error_code, "token":token}
    return JsonResponse(js)

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
        limit = request.POST.get('limit', 200)
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

    js = json.dumps({"error_code":error_code, 'data':data, "message":message},ensure_ascii=False)
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

    js = json.dumps({'event_list':event_list, 'error_code': error_code, 'message': message},ensure_ascii=False)
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
    event_detail=[]
    if request.method == 'GET':
        if is_sign(request):
            id = request.GET.get('id', None)
            if id:
                try:
                    event_detail = Event.objects.values('id', 'title', 'status',
                                                        'limit', 'address', 'time').get(id=id)
                    start_time = datetime.date.strftime(event_detail['time'], '%Y-%m-%d')
                    event_detail.pop('time')

                    error_code = '0'
                    message = ''
                except Exception as e:
                    print e
                    error_code='10004'
                    message = u'未查询到会议信息'
            else:
                error_code = '10001'
                message = u'缺少必填参数'
        else:
            error_code = '10011'
            message = u'签名错误'
    else:
        error_code = '10099'  # 请求类型错误
        message = u'请求类型错误'
    js = json.dumps({'event_detail': event_detail, 'error_code': error_code, 'message': message},ensure_ascii=False)
    return HttpResponse(js)

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
    error_code = ''
    message = ''
    if request.method == 'POST':
        if is_sign(request):
            id = request.POST.get('id', None)
            status = request.POST.get('status', None)
            if id and status:
                try:
                    status = int(status)
                    if status in (0, 1, 2):
                        try:
                            event = Event.objects.get(id=id)
                            event.status = status
                            event.save()
                            error_code = '0'

                        except:
                            error_code = '10004'
                            message =u'未查询到会议信息'
                    else:
                        error_code = '10003'
                        message = u'status类型不存在'
                except Exception as e:
                    print e
                    error_code = '10098'
                    message = u'数据类型错误'
            else:
                error_code = '10001'
                message = u'缺少必填参数'
        else:
            error_code = '10011'
            message = u'签名错误'
    else:
        error_code = '10099'
        message = u'请求类型错误'

    js = json.dumps({'error_code': error_code, 'message': message}, ensure_ascii=False)
    return HttpResponse(js)

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
@api_view(['POST'],)
def add_guest(request):
    data={}
    error_code = ''
    event_id = request.POST.get('id', None)
    name = request.POST.get('name', None)
    phone_number = request.POST.get('phone_number', None)
    email = request.POST.get('email', None)
    if event_id and name and phone_number:
        if is_sign(request):
            try:
                event = Event.objects.get(id=event_id)
                if Guest.objects.filter(phone_number=phone_number).exists():
                    guest = Guest.objects.get(phone_number=phone_number)
                    guest.name = name
                    if email:
                        guest.email = email
                    guest.save()
                else:
                    guest = Guest.objects.create(phone_number=phone_number, name=name, email=email)
                if Event.objects.filter(id=event_id,guest=guest).exists():
                    error_code = '10005'
                else:
                    print event
                    if event.guest.count() == event.limit:
                        error_code = '10006'
                    else:
                        event.guest.add(guest)
                        error_code = '0'
                        data["event_id"] = event.id
                        data["guest_id"] = guest.id
            except Exception as e:
                print e
                error_code = '10004'
        else:
            error_code = '10011'
    else:
        error_code = '10001'

    js = {'data': data, 'error_code': error_code}
    return JsonResponse(js)

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
@api_view(['GET'])
def get_guestlist(request):
    error_code = ''
    guest_list =[]
    event_id = request.GET.get('event_id', None)
    phone_number = request.GET.get('phone_number', None)
    if is_sign(request):
        if Event.objects.filter(id=event_id).exists():
            if phone_number:

                if Event.objects.filter(id=event_id,guest__phone_number=phone_number).exists():
                    guest = Guest.objects.values('id', 'name', 'phone_number', 'email').get(phone_number=phone_number)
                    guest_list = [{"guest_id": guest['id'], "name": guest['name'],
                                   "phone_number": guest['phone_number'], "email": guest['email']}]
            else:
                guest = Event.objects.get(id=event_id).guest.values('id', 'name', 'phone_number', 'email')

                guest_list = [{"guest_id": guest[0]['id'], "name": guest[0]['name'],
                               "phone_number": guest[0]['phone_number'], "email": guest[0]['email']}]

            error_code = 0

        else:
            error_code = '10004'
    else:
        error_code = '10011'

    js = {'guest_list': guest_list, 'error_code': error_code}
    return JsonResponse(js)

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
    error_code = ''


    js = {'error_code': error_code}
    return JsonResponse(js)