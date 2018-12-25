from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from landing import views

urlpatterns = [
    path('', views.home),
    path('setting/', views.setting, name='setting'),
    url(r'^setting/(?P<algorithm_id>[0-9]+)/$', views.setting_algorithm),
]
