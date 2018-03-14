from django.shortcuts import render

# Create your views here.

def home(request, id):
    #return HttpResponse('hello world')
    info = 'test' + id
    return render(request, 'demo2/home.html', {'info': info})

