#coding:utf-8
from django import VERSION

if VERSION[0:2]>(1,3):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url

from views import UploadFile

urlpatterns = patterns('',
    url(r'^upload/(?P<uploadpath>.*)', UploadFile, {'uploadtype':'image'}),
)
