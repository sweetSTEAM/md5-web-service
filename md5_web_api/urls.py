from django.conf.urls import url
from . import views

urlpatterns = [
    # /api/post_link/
    url(r'^post_link/$', views.post_link, name='post_link'),
    # /api/get_statis/<GUID>
    url(r'^get_status/(?P<guid>[a-z0-9-]+)/$', views.get_status,
        name='get_status')
]