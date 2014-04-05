#coding=utf-8

#修正输入的文件路径,输入路径的标准格式：abc,不需要前后置的路径符号
def FixFilePath(OutputPath, instance=None):
    if callable(OutputPath):
        try:
            OutputPath=OutputPath(instance)
        except:
            OutputPath = ""
    else:
        try:
            import datetime
            OutputPath = datetime.datetime.now().strftime(OutputPath)
        except:
            pass
        if len(OutputPath) > 0:
            OutputPath = "%s/" % OutputPath.strip("/")

    return OutputPath

#在上传的文件名后面追加一个日期时间+随机,如abc.jpg--> abc_20120801202409.jpg
def GenerateRndFilename(filename):
    import datetime
    import random
    from os.path import splitext
    f_name, f_ext=splitext(filename)
    return "%s_%s%s%s" % (f_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S_"),random.randrange(10,99),f_ext)

#文件大小类
class FileSize():
    SIZE_UNIT={"Byte":1,"KB":1024,"MB":1048576,"GB":1073741824,"TB":1099511627776L}
    def __init__(self,size):
        self.size=long(FileSize.Format(size))

    @staticmethod
    def Format(size):
        import re
        if isinstance(size,int) or isinstance(size,long):
            return size
        else:
            if not isinstance(size,str):
                return 0
            else:
                oSize=size.lstrip().upper().replace(" ","")
                pattern=re.compile(r"(\d*\.?(?=\d)\d*)(byte|kb|mb|gb|tb)",re.I)
                match=pattern.match(oSize)
                if match:
                    m_size, m_unit=match.groups()
                    if m_size.find(".")==-1:
                        m_size=long(m_size)
                    else:
                        m_size=float(m_size)
                    if m_unit!="BYTE":
                        return m_size*FileSize.SIZE_UNIT[m_unit]
                    else:
                        return m_size
                else:
                    return 0

    #返回字节为单位的值
    @property
    def size(self):
        return self.size
    @size.setter
    def size(self,newsize):
        try:
            self.size=long(newsize)
        except:
            self.size=0

    #返回带单位的自动值
    @property
    def FriendValue(self):
        if self.size<FileSize.SIZE_UNIT["KB"]:
            unit="Byte"
        elif self.size<FileSize.SIZE_UNIT["MB"]:
            unit="KB"
        elif self.size<FileSize.SIZE_UNIT["GB"]:
            unit="MB"
        elif self.size<FileSize.SIZE_UNIT["TB"]:
            unit="GB"
        else:
            unit="TB"

        if (self.size % FileSize.SIZE_UNIT[unit])==0:
            return "%s%s" % ((self.size / FileSize.SIZE_UNIT[unit]),unit)
        else:
            return "%0.2f%s" % (round(float(self.size) /float(FileSize.SIZE_UNIT[unit]) ,2),unit)

    def __str__(self):
        return self.FriendValue

    #相加
    def __add__(self, other):
        if isinstance(other,FileSize):
            return FileSize(other.size+self.size)
        else:
            return FileSize(FileSize(other).size+self.size)
    def __sub__(self, other):
        if isinstance(other,FileSize):
            return FileSize(self.size-other.size)
        else:
            return FileSize(self.size-FileSize(other).size)
    def __gt__(self, other):
        if isinstance(other,FileSize):
            if self.size>other.size:
                return True
            else:
                return False
        else:
            if self.size>FileSize(other).size:
                return True
            else:
                return False
    def __lt__(self, other):
        if isinstance(other,FileSize):
            if other.size>self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size > self.size:
                return True
            else:
                return False
    def __ge__(self, other):
        if isinstance(other,FileSize):
            if self.size>=other.size:
                return True
            else:
                return False
        else:
            if self.size>=FileSize(other).size:
                return True
            else:
                return False
    def __le__(self, other):
        if isinstance(other,FileSize):
            if other.size>=self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size >= self.size:
                return True
            else:
                return False

def MadeSimditorOptions(width=600,height=300,toolbars="normal",
        filePath="",imagePath="",scrawlPath="",css="",options={}):
    import settings as Settings
    sOptions={}
    sOptions['css']=css
    if not imagePath:
        imagePath =Settings.SimditorSettings["images_upload"].get("path","")
    if not filePath:
        filePath  =Settings.SimditorSettings["files_upload"].get("path","")

    sOptions['imagePath']=FixFilePath(imagePath)
    sOptions['filePath'] =FixFilePath(filePath)

    sOptions['O_imagePath']=imagePath
    sOptions['O_filePath']=filePath
    sOptions['toolbars']=toolbars
    sOptions['options']=options
    sOptions['width']=width
    sOptions['height']=height
    return sOptions
