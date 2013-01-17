#coding=utf-8
#
#from mogu.interface import InfoAll, InfoUpdate, InitApp, ChangeAppData, AddReply
#from mogu.subscribe import SubscribeList, SubscribeAdd, SubscribeInfo, UserSubscribeAdd, SubscribeDelete, SubscribeStatus
#from mogu.users import UserInfo, UserAdd, UserDelete, UserUpdate, UserList, UserLogin, UserRegister
#from mogu.weibo import WeiboCheck
from imglib.img import Group, PicAdd, PicList, ShowImg, UserGroup, UserGroupApply, DownImg
from imglib.interface import SendGroup, InfoAll, InfoAllImg

__author__ = u'王健'
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
#from google.appengine.ext.webapp import util
#from mogu.content import ContentList, ContentAdd, ContentUpdate, ContentDelete
#from mogu.login import Login, Top, Menu

app = webapp2.WSGIApplication([
    ('/group', Group),
    ('/usergroup', UserGroup),
    ('/groupapply', UserGroupApply),
    ('/picadd', PicAdd),
    ('/piclist', PicList),
    ('/picshow', ShowImg),
    ('/sendgroup', SendGroup),
    ('/InfoUpdate', InfoAllImg),
    ('/InfoAll', InfoAll),
    ('/downLoad', DownImg),
#    ('/login', Login),
#    ('/top',Top),
#    ('/menu',Menu),
#    ('/contentList/(?P<page>[0-9]*)',ContentList),
#    ('/contentAdd',ContentAdd),
#    ('/contentUpdate',ContentUpdate),
#    ('/contentDelete',ContentDelete),
#    ('/userList/(?P<page>[0-9]*)',UserList),
#    ('/userInfo',UserInfo),
#    ('/userAdd',UserAdd),
#    ('/userDelete',UserDelete),
#    ('/userUpdate',UserUpdate),
#    ('/subscribeInfo', SubscribeInfo),
#    ('/subscribeList/(?P<page>[0-9]*)', SubscribeList),
#    ('/subscribeAdd', SubscribeAdd),
#    ('/userSubscribeAdd', UserSubscribeAdd),
#    ('/subscribeDelete',SubscribeDelete),
#    ('/subscribeStatus',SubscribeStatus),
#
#    ('/init',InitApp),
#
#    ('/InfoAll',InfoAll),
#    ('/InfoUpdate',InfoUpdate),
#    ('/UserLogin', UserLogin),
#    ('/UserRegister', UserRegister),
#    ('/AddReply', AddReply),
#
#    #改变应用的配置
#    ('/changeAppData',ChangeAppData),
#    ('/WeiboCheck',WeiboCheck),

                              ],
                                         debug=True)
def main():
    pass

#    util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
