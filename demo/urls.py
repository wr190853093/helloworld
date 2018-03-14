from django.conf.urls import include, url

urlpatterns = [
    url(r'^home/', 'demo.views.home'),
    url(r'^bugs/', 'demo.views.bugs'),
    url(r'^login/', 'demo.views.login'),
    url(r'^index/', 'demo.views.index')
]