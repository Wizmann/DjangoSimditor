#coding: utf-8

from django import forms
from widgets import SimditorWidget
from utils import MadeSimditorOptions

class SimditorField(forms.CharField):
    def __init__(self,label,width=600,height=300,plugins=(),toolbars="normal",filePath="",imagePath="",css="",options={}, *args, **kwargs):
        sOptions=MadeSimditorOptions(width,height,plugins,toolbars,filePath,imagePath,css,options)
        kwargs["widget"]=SimditorWidget(**uOptions)
        kwargs["label"]=label
        super(SimditorField,self).__init__( *args, **kwargs)

def UpdateUploadPath(widget,model_inst=None):
    try:
        from DjangoSimditor.models import SimditorField as ModelSimditorField
        for field in model_inst._meta.fields:
            if isinstance(field, ModelSimditorField):
                if  callable(field.simditor_options["O_imagePath"]):
                    newPath=field.simditor_options["O_imagePath"](model_inst)
                    widget.__getitem__(field.name).field.widget.simditor_options["imagePath"] =newPath
                    if not field.simditor_options["O_imageManagerPath"]:
                        widget.__getitem__(field.name).field.widget.simditor_options["imageManagerPath"] = newPath
                    if not field.simditor_options["O_scrawlPath"]:
                        widget.__getitem__(field.name).field.widget.simditor_options["scrawlPath"] = newPath
                if  callable(field.ueditor_options["O_filePath"]):
                    widget.__getitem__(field.name).field.widget.ueditor_options["filePath"] =field.simditor_options["O_filePath"](model_inst)
                if  callable(field.ueditor_options["O_imageManagerPath"]):
                    widget.__getitem__(field.name).field.widget.ueditor_options["imageManagerPath"] =field.simditor_options["O_imageManagerPath"](model_inst)
                if  callable(field.ueditor_options["O_scrawlPath"]):
                    widget.__getitem__(field.name).field.widget.ueditor_options["scrawlPath"] =field.simditor_options["O_scrawlPath"](model_inst)
    except:
        pass

class SimditorModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(SimditorModelForm,self).__init__(*args,**kwargs)
        try:
            if kwargs.has_key("instance"):
                UpdateUploadPath(self,kwargs["instance"])
            else:
                UpdateUploadPath(self,None)
        except Exception:
            pass
