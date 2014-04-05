from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from testApp.views import HomeView, BlogCreateView, BlogUpdateView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^create/$', BlogCreateView.as_view(), name='create_blog_view'),
    url(r'^update/(?P<pk>\d+)/$', csrf_exempt(BlogUpdateView.as_view()), name='update_blog_view'),
)
