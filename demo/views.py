#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from init_db.models import *
import method
from models import *
# Create your views here.

def index(request):

    if request.COOKIES:
        username = request.COOKIES.get('username')
        pwd = request.COOKIES.get('pwd')
        # print username
        if username:
            info = u'登录成功，欢迎%s' % username
            return render(request, 'home.html', {'info': info})
    else:
        return render(request, 'login.html')

        # return HttpResponse("{'info':'123'}",content_type='json')
        # return render(request, 'login.html')
        # 增
        # Author(name='鲁迅').save()
        # Author.objects.create(name='李清照')
        # author = Author.objects.get(name='鲁迅')
        # AuthorDetails(age=18, sex=0, email='123@163.com', phone='13811111111', author=author).save()
        # 查
        # Author.objects.filter(name='李白')
        # author1 = Author.objects.filter(name__startswith='李')
        # for a in author1:
        #     print a
        # 删除
        # author = Author().objects.filter(name='李白').delete()
        # 级联删除
        # Author(name='李白').delete()
        # update
        # Author.objects.filter(name='李白').update(name='李黑')
        # return HttpResponse('1')

def home(request):

    if request.method == 'GET':
        pwd = request.GET.get('pwd')
        username = request.GET.get('name')
        if pwd and username:
            info = u'欢迎登录' + username
            return render(request, 'home.html', {'info':info})
        else:
            info = u'用户名\密码不能为空'
            return render(request,'error.html',{'info':info})
    elif request.method == 'POST':
        pwd = request.POST.get('pwd')
        username = request.POST.get('name')
        if pwd and username:
            info = u'欢迎登录' + username
            return render(request, 'home.html', {'info': info})
        else:
            info = u'用户名\密码不能为空'
            return render(request, 'error.html', {'info': info})
    else:
        info = u'请求类型错误'
        return render(request, 'error.html',{'info':info})

def bugs(request):

    month = request.GET.get('month',None)
    if month:
        try:
            month = int(month)
            if month in range(1,10):
                month = '2016_0' + str(month)
                total = method.get_total(month)
                info = u'%s月bug总数为:%d' % (month, total)

            elif month in range(10,13):
                month = '2016_' + str(month)
                total = method.get_total(month)
                info = u'%s月bug总数为%d' % (month, total)
            else:
                info = u'month参数无效'


        except:
            info = u'month参数无效11'
    else:

        info = u'month参数为必填参数'

    # return HttpResponse(content="{'info':%s}"%info, content_type='application/json')
    return render(request,'home.html',{'info': info})

def login(request):
    response = HttpResponse()

    if request.method == 'POST':
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        is_save = request.POST.get('is_save')
        # username = request.GET.get('username', None)
        # pwd = request.GET.get('getpassword', None)

        if username and pwd :

            if len(username) >= 5:
                user = method.get_login_stat(username,pwd)
                # user = auth.authenticate(username=username, password=pwd)
                if user:
                    info = u'登录成功，欢迎%s' % username
                    # response = render(request,'home.html',{'info': info})
                    if is_save:
                        response.set_cookie('username', username , max_age=300)
                        response.set_signed_cookie('pwd', pwd ,salt='123',max_age=300)
                    # return response

                else:
                    info = u'用户名或密码错误。'
            else:

                info = u'用户名位数不足5位。'
        else:
            # return HttpResponse(u'请输入用户名或密码。',status=400)
            info = u'请输入用户名或密码。'
    else:
        info = u'请求类型错误'
    response.content = info
    return response