#coding: utf-8
from django.db import models
from django.contrib.admin import widgets as admin_widgets
from widgets import SimditorWidget,AdminSimditorWidget
from utils import MadeSimditorOptions


class SimditorField(models.TextField):
    def __init__(self,verbose_name=None,
            width=600,height=300,plugins=(),toolbars="normal",
            filePath="",imagePath="",
            css="",options={},**kwargs):
        self.simditor_options=MadeSimditorOptions(width,height,plugins,toolbars,filePath,imagePath,css,options)
        kwargs["verbose_name"]=verbose_name
        super(SimditorField,self).__init__(**kwargs)

    def formfield(self,**kwargs):
        defaults = {'widget': SimditorWidget(**self.simditor_options)}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = AdminSimditorWidget(**self.ueditor_options)
        return super(SimditorField, self).formfield(**defaults)

