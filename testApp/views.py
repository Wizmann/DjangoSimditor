#coding=utf-8
from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from testApp.models import Blog

class HomeView(ListView):
    context_object_name = 'blog_list'
    queryset = Blog.objects.all()
    template_name = 'home.html'
    
class BlogFormView(View):
    model = Blog
    template_name = "form.html"
    success_url = reverse_lazy('home_view')

class BlogCreateView(BlogFormView, CreateView):
    pass

class BlogUpdateView(BlogFormView, UpdateView):
    pass

