#coding:utf-8
from django.shortcuts import render,HttpResponse

# Create your views here.

#验证签名
'''
根据传的参数进行解密，判断签名是否正确
'''
def is_sign(sign):
    flag = False

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
'''
def add_event(request):
    response = HttpResponse()

    return response

#查询会议列表
'''
校验内容：
1、校验请求类型
2、根据title判断全查询，还是按标题模糊查询
3、查询列表为空，返回错误码10004
4、校验签名是否正确

校验结果，按接口文档返回对应参数
'''
def get_eventlist(request):
    response = HttpResponse()

    return response

#查询会议详细信息
'''
校验内容：
1、校验请求类型
2、校验id参数是否填写
3、根据id查找会议信息
4、校验签名是否正确

校验结果，按接口文档返回对应参数
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
'''
def sign(request):
    response = HttpResponse()

    return response