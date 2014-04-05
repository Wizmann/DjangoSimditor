# coding=utf-8
from django.conf import settings as gSettings #全局设置

#工具栏样式，可以添加任意多的模式
TOOLBARS_SETTINGS= {
    "normal": ['title', 'bold', 'italic', 'underline', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent'],
}

#允许上传的图片类型
UPLOAD_IMAGES_SETTINGS={
    "allow_type":"jpg,bmp,png,gif,jpeg",         #文件允许格式
    "path":"",
    "max_size":0                                #文件大小限制，单位KB,0不限制
}
#允许上传的附件类型
UPLOAD_FILES_SETTINGS={
    "allow_type":"zip,rar,doc,docx,xls,xlsx,ppt,pptx,swf,dat,avi,rmvb,txt,pdf",         #文件允许格式
    "path":"",
    "max_size":0                               #文件大小限制，单位KB,0不限制
}

SimditorSettings={
    "toolbars":      TOOLBARS_SETTINGS,
    "images_upload": UPLOAD_IMAGES_SETTINGS,
    "files_upload":  UPLOAD_FILES_SETTINGS,
}

#更新配置：从用户配置文件settings.py重新读入配置UEDITOR_SETTINGS,
def UpdateUserSettings():
    UserSettings=getattr(gSettings,"SIMDITOR_SETTINGS",{}).copy()
    for k in SimditorSettings.iterkeys():
        try:
            SimditorSettings[k].update(UserSettings.pop(k,{}))
        except Exception:
            pass
    SimditorSettings.update(UserSettings)

#取得配置项参数
def GetSimditorSettings(key,default=None):
    if SimditorSettings.has_key(key):
        return SimditorSettings[key]
    else:
        return default

#读取用户Settings文件覆盖默认配置
UpdateUserSettings()
