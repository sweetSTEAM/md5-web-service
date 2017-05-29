from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^api/', include('md5_web_api.urls')),
    url(r'^$', views.index, name='index')
]
