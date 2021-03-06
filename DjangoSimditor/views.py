#coding:utf-8

import os
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

import settings as Settings
from utils import GenerateRndFilename
from utils import FileSize


#保存上传的文件
def SaveUploadFile(PostFile,FilePath):
    with open(FilePath, 'wb') as f:
        try:
            for chunk in PostFile.chunks():
                f.write(chunk)
        except Exception,E:
            return u"写入文件错误:"+ E.message
    return u"SUCCESS"

#上传附件
@csrf_exempt
def UploadFile(request, uploadtype, uploadpath):
    if request.method != "POST":
        return  HttpResponse(simplejson.dumps( u"{'state:'METHOD ERROR'}"),mimetype="Application/javascript")
    state="SUCCESS"
    file=request.FILES.get("upload_file",None)
    #如果没有提交upfile则返回错误
    if file is None:
        return HttpResponse(simplejson.dumps(u"{'state:'FILE ERROR'}") ,mimetype="Application/javascript")
    #取得上传的文件的原始名称
    original_name,original_ext=os.path.splitext(file.name)
    original_ext=original_ext[1:]
    #类型检验
    if uploadtype=="image":
        allow_type= Settings.SimditorSettings["images_upload"]['allow_type']
    else:
        allow_type= Settings.SimditorSettings["files_upload"]['allow_type']
    if not original_ext  in allow_type:
        state=u"服务器不允许上传%s类型的文件。" % original_ext
    #大小检验
    max_size=Settings.SimditorSettings["images_upload"]['max_size']
    if max_size!=0:
        MF=FileSize(max_size)
        if file.size>MF.size:
            state=u"上传文件大小不允许超过%s。" % MF.FriendValue
    #检测保存路径是否存在,如果不存在则需要创建
    OutputPath=os.path.join(Settings.gSettings.MEDIA_ROOT, os.path.dirname(uploadpath)).replace("//","/")
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
        #要保存的文件名格式使用"原文件名_当前时间.扩展名"
    OutputFile=GenerateRndFilename(file.name)
    
    #所有检测完成后写入文件
    if state=="SUCCESS":
        #保存到文件中
        state=SaveUploadFile(file,os.path.join(OutputPath,OutputFile))
    #返回数据
    
    OutputFile = Settings.gSettings.MEDIA_URL + uploadpath + OutputFile

    if uploadtype=="image":
        rInfo={
            'file_path'      :OutputFile,    #保存后的文件名称
        }
    else:
        rInfo={
            'file_path'      :OutputFile,         #保存后的文件名称
        }
    return HttpResponse(simplejson.dumps(rInfo),mimetype="application/json")
