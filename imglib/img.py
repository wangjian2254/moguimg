#coding=utf-8
#author:u'王健'
#Date: 12-2-11
#Time: 下午3:49
import logging
import datetime
from imglib.model.models import Img, ImgGroup, User
from tools.page import Page
from google.appengine.api.images import Image
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.api import  memcache
import urllib

__author__ = u'王健'

class PicAdd(Page):
    def get(self):
        imgid=self.request.get("imgid") or ''
        group=None
        groupid=self.request.get('groupid') or ''
        if groupid:
            groupid=int(groupid)
            group=ImgGroup.get_by_id(int(groupid))
        grouplist=ImgGroup.all().order('-updateTime')
        self.render('templates/picadd.html',{'groupid':groupid,'group':group,'grouplist':grouplist,'imgid':imgid})
    def post(self):
        if self.request.get('pic'):
            imgdata=self.request.get('pic')
            imgid=self.request.get("imgid") or ''
            logging.info('0'+str(imgid))
            img=Image(imgdata)
            group=self.request.get('group')

            pama=urllib.unquote(self.request.body)
            logging.info('1'+str(pama))
            #filename="11575.gif"
            s='filename="'
            n=pama.find(s)+len(s)
            nn=pama.find('"',n)
            pama=pama[n:nn]
#            pama=pama[pama.find('pic'):].split("&")
#            logging.info('2'+str(pama))
#
#            pama=pama[0].split('=')
#            logging.info('3'+str(pama))
#            pama=pama[1].split(',')[1]
#            logging.info('4'+str(pama))
#            pama=pama[pama.find("'")+1:pama.rfind(",")-1]
#            logging.info('5'+str(pama))
            type=pama.split('.')[1]
            logging.info('6'+str(pama))
            if type:
                type=type.lower()


            if img:
#                imgdata=img._image_data
                if img.width>350 and type!='gif':
                    imgdata=images.resize(imgdata,width=350)

                if imgid:
                    entity = Img.get_by_id(int(imgid))
                    if entity:
                        entity.ver+=1
                else:
                    entity = Img()
                entity.afile = db.Blob(imgdata)
                entity.group=int(group)
                if type=='gif':
                    entity.type='image/gif'
                elif type=='png':
                    entity.type='image/png'
                entity.put()
        self.redirect(str('/picadd'+'?groupid='+group))

class ShowImg(Page):
    def get(self):
        imgid=self.request.get("imgid")
        if not imgid:
            self.error(500)
            return
        image=Img.get_by_id(int(imgid))
        if image:
            self.response.headers['Content-Type'] = str(image.type)
            self.response.out.write(image.afile)
        else:
            self.error(505)


class DownImg(Page):
    def get(self):
        imgid=self.request.get("image_id")
        if imgid:
            imgidlist=imgid.split('_')
            if (len(imgidlist)==3 or len(imgidlist)==4) and imgidlist[-1] in ['11','12','31','41']:
                if imgidlist[0] in ['min','daily','weekly','monthly']:
                    self.response.headers['Content-Type'] = "text/html"
                    if imgidlist[-1]=='41':
#                        self.response.out.write('http://image.sinajs.cn/newchart/usstock/%s/%s.gif'%(imgidlist[0],imgidlist[-2]))
                        if 'min'==imgidlist[0]:
                            self.response.out.write('http://image.sinajs.cn/newchart/v5/usstock/wap/min_daily/310/%s.gif?r=%s'%(imgidlist[-2],datetime.datetime.now().strftime('%Y%m%d%H%M')))
                        if 'daily'==imgidlist[0]:
                            self.response.out.write('http://image.sinajs.cn/newchart/v5/usstock/wap/min_week/310/%s.gif?r=%s'%(imgidlist[-2],datetime.datetime.now().strftime('%Y%m%d%H%M')))
                        return
                    elif imgidlist[-1]=='31':
#                        self.response.out.write('http://image.sinajs.cn/newchart/hk_stock/%s/%s.gif'%(imgidlist[0],imgidlist[-2][2:]))
                        if 'min'==imgidlist[0]:
                            self.response.out.write('http://r3.sinaimg.cn/3g/static/images/finance/hkstock/wap_min5/%s.gif?r=%s'%(imgidlist[-2][2:],datetime.datetime.now().strftime('%Y%m%d%H%M')))
                        if 'daily'==imgidlist[0]:
                            self.response.out.write('http://r3.sinaimg.cn/3g/static/images/finance/hkstock/daily_wap5/%s.gif?r=%s'%(imgidlist[-2][2:],datetime.datetime.now().strftime('%Y%m%d%H%M')))

                        return
                    elif imgidlist[-1] in ['11','12']:
#                        self.response.out.write('http://image.sinajs.cn/newchart/%s/n/%s.gif'%(imgidlist[0],imgidlist[-2]))
                        if 'min'==imgidlist[0]:
                            self.response.out.write('http://r3.sinaimg.cn/3g/static/images/finance/stock/daily2/3g/big/%s.gif?r=%s'%(imgidlist[-2],datetime.datetime.now().strftime('%Y%m%d%H%M')))
                        if 'daily'==imgidlist[0]:
                            self.response.out.write('http://r3.sinaimg.cn/3g/static/images/finance/stock/k/daily2/3g/big/%s.gif?r=%s'%(imgidlist[-2],datetime.datetime.now().strftime('%Y%m%d%H%M')))
                        return
                    else:
                        self.error(500)
                        return
        if not imgid or imgid[0]=='0':
            self.error(500)
            return
        image=Img.get_by_id(int(imgid))
        if image:
            self.response.headers['Content-Type'] = str(image.type)
            self.response.out.write(image.afile)
        else:
            self.error(505)

class PicList(Page):
    def get(self):
        groupid=self.request.get('groupid')
        group=ImgGroup.get_by_id(int(groupid))
        imglist=[]
        if group:
            imglist=Img.all().filter('group =',group.key().id()).order('-__key__').fetch(10)

        self.render('templates/piclist.html',{'group':group,'imglist':imglist})

class Group(Page):
    def get(self):
        updateid=self.request.get('groupid') or ''
        group=''
        if updateid:
            group=ImgGroup.get_by_id(int(updateid))
            if group:
                group=group.group
        grouplist=ImgGroup.all().order('-updateTime')
        self.render('templates/group.html',{'grouplist':grouplist,'updateid':updateid,'group':group})
    def post(self):
        group=self.request.get('group')
        groupid=self.request.get('id')
        if group:
            g=None
            if groupid:
                g=ImgGroup.get_by_id(int(groupid))
            if not g:
                g=ImgGroup()
            g.group=group
            g.lib='sys'
            g.put()
        self.redirect('/group')

class UserGroup(Page):
    def get(self):
        user=self.request.get('UserName') or '000'
        if user:
            u=User.get_by_key_name('u'+user)
            grouplist=[]
            if u:
                grouplist=ImgGroup.get_by_id(u.grouplist)
            self.render('templates/groupuser.html',{'usergrouplist':grouplist,'grouplist':ImgGroup.all()})
class UserGroupApply(Page):
    def get(self):
        do=self.request.get('do')
        groupid=self.request.get('groupid')
        if not do and not groupid:
            return
        if groupid:
            groupid=int(groupid)

        u=User.get_by_key_name('u000')
        if not u:
            u=User(key_name='u000')
            u.put()
        if do=='del':
            u.grouplist.remove(groupid)
            u.put()
        if do=='add':
            if groupid not in u.grouplist:
                u.grouplist.append(groupid)
                u.put()
        self.redirect('/usergroup')



  