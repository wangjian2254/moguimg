#coding=utf-8
#author:u'王健'
#Date: 12-2-11
#Time: 下午1:14
__author__ = u'王健'


from google.appengine.ext import db

class Img(db.Model):
    group=db.IntegerProperty()
    ver=db.IntegerProperty(indexed=False,default=0)
    type=db.StringProperty(indexed=False,default='image/jpeg')
    afile=db.BlobProperty()
class ImgGroup(db.Model):
    lib=db.StringProperty(default='sys')#库名
    group=db.StringProperty()
    updateTime=db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
    grouplist=db.ListProperty(item_type=int,indexed=False)

