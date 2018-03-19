from django.conf.urls import include, url

urlpatterns = [
    url(r'^register/', 'api.views.register'),
    url(r'^add_event/', 'api.views.add_event'),
    url(r'^get_eventlist/', 'api.views.get_eventlist'),
    url(r'^get_eventdetail/', 'api.views.get_eventdetail'),
    url(r'^set_status/', 'api.views.set_status'),
    url(r'^add_guest/', 'api.views.add_guest'),
    url(r'^get_guestlist/', 'api.views.get_guestlist'),
    url(r'^sign/', 'api.views.sign'),

]