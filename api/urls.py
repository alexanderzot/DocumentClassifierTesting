from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'files/$', ListFileView.as_view()),
    url(r'file/(?P<pk>[0-9]+)/$', DetailFileView.as_view()),
    url(r'user/sign_in/$', user_sign_in, name='sign_in'),
    url(r'user/sign_out/$', user_sign_out, name='sign_out'),
    url(r'user/sign_up/$', user_sign_up, name='sign_up'),
]
