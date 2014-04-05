#coding=utf-8
from django.db import models
from DjangoSimditor.models import SimditorField

class Blog(models.Model):
    title = models.CharField(max_length=32, verbose_name=u'博客标题') 
    content = SimditorField(verbose_name=u'博客正文', imagePath='upload/', filePath='upload/')
     
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u'博客'
        ordering = ['-id']
