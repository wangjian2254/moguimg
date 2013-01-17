#coding=utf-8
#author:u'王健'
#Date: 12-2-18
#Time: 下午4:28
import logging
from xml.dom.minidom import Document
from imglib.model.models import User, Img, ImgGroup
from setting import APPCODE, IMGURI, APPCODE_ID
from tools.page import Page

__author__ = u'王健'

def infoallimgxmldic(contents,xml=None,lib=None,groupid='',grouptxt=''):
    if not xml:
        xml=Document()
        images=xml.createElement('images')
        images.setAttribute('codeid',APPCODE_ID)
        images.setAttribute('code',APPCODE)
        images.setAttribute('type','infoupdate')
        images.setAttribute('timespan',str(24*3600))
        xml.appendChild(images)
        lib=xml.createElement('lib')
        lib.setAttribute('name','sys')
        images.appendChild(lib)
    group=xml.createElement('group')
    group.setAttribute('name',str(groupid))
    group.setAttribute('text',grouptxt)
    lib.appendChild(group)
    for c in contents:
        if not c:
            continue
        img=xml.createElement('img')
        img.setAttribute('id',str(c.key().id()))
        img.setAttribute('var',str(c.ver))
#        if not delete and c.status=='1':
#            data.setAttribute('code',c.key().name() or '')
#            data.setAttribute('father',c.father or '')
#            if c.title:
#                data.setAttribute('title',c.title or '')
#            if c.updateSpanTime:
#                data.setAttribute('updateSpanTime',c.updateSpanTime or '')
#            if c.replyType:
#                data.setAttribute('replyType',c.replyType or '')
#            data.setAttribute('maincode',c.maincode or '')
#            data.setAttribute('level',c.level or '')
#            data.appendChild(xml.createTextNode(c.content or ''))
#            data.setAttribute('status',c.status or '')
#            data.setAttribute('lastUpdateTime',str(c.lastUpdateTime) or '')
#        else:
#            if type(c) is str or type(c) is unicode:
#                data.setAttribute('code',c)
#            else:
#                data.setAttribute('code',c.key().name() or '')
#            data.setAttribute('status','0' or '')
        group.appendChild(img)
    return (xml,lib)

class InfoAllImg(Page):
    def get(self):
        uname=self.request.get('UserName') or ''
        xml=None
        lib=None
        if uname:
            grouplist=[]
            u=User.get_by_key_name('u'+uname)
            if u:
                grouplist+=u.grouplist
            u=User.get_by_key_name('u000')
            if u:
                grouplist+=u.grouplist
            for group in grouplist:
                imglist=Img.all().filter('group =',group)
                grouptxt=ImgGroup.get_by_id(group).group
                xml,lib=infoallimgxmldic(imglist,xml,lib,group,grouptxt)
            if xml:
                self.response.out.write(xml.toxml('utf-8'))
class InfoAll(Page):
    def get(self):
        uname=self.request.get('UserName') or ''
        replayType='21'
        idset=set()
        contentlist=[]
        getMapList(contentlist,APPCODE+'-s1',APPCODE,'',APPCODE,'100',u'图片组','','1',replayType)
        if uname:
            u=User.get_by_key_name('u000')
            for ugid in u.grouplist:
                if ugid not in idset:
                    imggroup=ImgGroup.get_by_id(ugid)
                    getMapList(contentlist,APPCODE+'-s1-'+str(imggroup.key().id()),APPCODE+'-s1','',APPCODE,'101',imggroup.group+u'(默认)',imggroup.updateTime,'1',replayType)
                    idset.add(ugid)
            u=User.get_by_key_name('u'+uname)
            if u:
                for ugid in u.grouplist:
                    if ugid not in idset:
                        imggroup=ImgGroup.get_by_id(ugid)
                        getMapList(contentlist,APPCODE+'-s1-'+str(imggroup.key().id()),APPCODE+'-s1','',APPCODE,'101',imggroup.group+u'(已下载)',imggroup.updateTime,'1',replayType)
                        idset.add(ugid)
        for imggroup in ImgGroup.all():
            if imggroup.key().id() not in idset:
                getMapList(contentlist,APPCODE+'-s1-'+str(imggroup.key().id()),APPCODE+'-s1','',APPCODE,'101',imggroup.group,imggroup.updateTime,'1',replayType)
                idset.add(ugid)
        xml,datas=infoallxmldic(contentlist)
        self.response.out.write(xml.toxml('utf-8'))




def infoallxmldic(contents,xml=None,datas=None,delete=None):
    if not xml:
        xml=Document()
        datas=xml.createElement('datas')
        datas.setAttribute('code',APPCODE)
        datas.setAttribute('type','infoall')
        datas.setAttribute('timespan',str(24*3600*2))
        #datas.setAttribute('time','%s' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#        datas.setAttribute('type','infoall')
        xml.appendChild(datas)
    for c in contents:
        if not c:
            continue
        data=xml.createElement('data')
        if not delete and c['status']=='1':
            data.setAttribute('code',c['code'] or '')
            data.setAttribute('father',c['father'] or '')
            if c.has_key('title'):
                data.setAttribute('title',c['title'] or '')
            if c.has_key('updateSpanTime'):
                data.setAttribute('updateSpanTime',c['updateSpanTime'] or '')
            if c.has_key('replyType'):
                data.setAttribute('replyType',c['replyType'] or '')
            data.setAttribute('maincode',c['maincode'] or '')
            data.setAttribute('level',c['level'] or '')
            data.appendChild(xml.createTextNode(c['content'] or ''))
            data.setAttribute('status',c['status'] or '')
            data.setAttribute('lastUpdateTime',str(c['lastUpdateTime']) or '')
        else:
            if type(c) is str:
                data.setAttribute('code',c)
            else:
                data.setAttribute('code',c['code'] or '')
            data.setAttribute('status','0' or '')
        datas.appendChild(data)
    return (xml,datas)

def getMapList(l,code,father,title,maincode,level,content,lastUpdateTime,status,replyType):
    u={}
    u['code']=code
    u['father']=father
    u['title']=title
    u['maincode']=maincode
    u['level']=level
    u['content']=content
    u['lastUpdateTime']=lastUpdateTime
    u['status']=status
    u['replyType']=replyType
    l.append(u)

    
class SendGroup(Page):
    def get(self):
        uname=self.request.get('UserName') or ''
        groupid=self.request.get('groupid') or None
        code=self.request.get('Code') or None
        if not groupid and code:
            groupid=code.split('-')[-1]
        if uname and groupid:
            u=User.get_by_key_name('u'+uname)
            groupid=int(groupid)
            if u:
                if groupid not in u.grouplist:
                    u.grouplist.append(groupid)
                    u.put()
            else:
                u=User(key_name='u'+uname)
                u.grouplist.append(groupid)
                u.put()
        self.response.out.write(self.request.host+'/InfoUpdate')

class ShowImg(Page):
    def get(self):
        imgid=self.request.get("image_id")
        if not imgid:
            self.error(500)
            return
        greeting = memcache.Client().get(str(imgid))
        logging.info(imgid)
        logging.info(str(imgid))
        if not greeting:
            self.error(404)
        elif greeting!='noimg':
            self.response.headers['Content-Type'] = "application/x-www-form-urlencoded"
            self.response.out.write(greeting)
        else:
            self.error(505)