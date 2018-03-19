from django.shortcuts import render,HttpResponse

# Create your views here.

#系统管理员登录
def register(request):
    response = HttpResponse()

    return response

#添加会议
def add_event(request):
    response = HttpResponse()

    return response

#查询会议列表
def get_eventlist(request):
    response = HttpResponse()

    return response

#查询会议详细信息
def get_eventdetail(request):
    response = HttpResponse()

    return response

#修改会议状态
def set_status(request):
    response = HttpResponse()

    return response

#添加嘉宾
def add_guest(request):
    response = HttpResponse()

    return response

#查询会议嘉宾
def get_guestlist(request):
    response = HttpResponse()

    return response

# 嘉宾签到
def sign(request):
    response = HttpResponse()

    return response