#coding:utf-8
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils import simplejson

from utils import MadeSimditorOptions
import settings as Settings

class SimditorWidget(forms.Textarea):
    def __init__(self, width=600, height=300, toolbars="normal",
            filePath="", imagePath="", css="",
            options={}, attrs=None, **kwargs):
        self.simditor_options=MadeSimditorOptions(width,height,toolbars,filePath,imagePath,css,options)
        super(SimditorWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        #取得工具栏设置
        try:
            if type(self.simditor_options['toolbars'])==list:
                tbar=simplejson.dumps(self.simditor_options['toolbars'])
            else:
                if getattr(Settings,"TOOLBARS_SETTINGS",{}).has_key(str(self.simditor_options['toolbars'])):
                    if self.simditor_options['toolbars'] =="full":
                        tbar=None
                    else:
                        tbar=simplejson.dumps(Settings.TOOLBARS_SETTINGS[str(self.simditor_options['toolbars'])])
                else:
                    tbar=None
        except:
            pass

        #传入模板的参数
        sOptions=self.simditor_options.copy()
        sOptions.update({
            "name":name,
            "value":conditional_escape(force_unicode(value)),
            "toolbars":tbar,
            "options":simplejson.dumps(self.simditor_options['options'])[1:-1]
        })
        context = {
                'Simditor'    : sOptions,
                'STATIC_URL'  : settings.STATIC_URL,
                'STATIC_ROOT' : settings.STATIC_ROOT,
                'MEDIA_URL'   : settings.MEDIA_URL,
                'MEDIA_ROOT'  : settings.MEDIA_ROOT
        }
        return mark_safe(render_to_string('simditor.html',context))
        
    class Media:
        css={"all": (
                "simditor/styles/simditor.css",
                "simditor/styles/font-awesome.css" ,
            )}
        js=("simditor/scripts/jquery-2.1.0.min.js",
            "simditor/scripts/module.js",
            "simditor/scripts/simditor-all.js",)



class AdminSimditorWidget(AdminTextareaWidget, SimditorWidget):
    def __init__(self, **kwargs):
        self.simditor_options = kwargs
        super(SimditorWidget,self).__init__(kwargs)
