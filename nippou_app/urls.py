#!coding:utf-8
__author__ = 'tie304184'

from django.conf.urls import patterns, url
from nippou_app import views

urlpatterns = patterns('',
        url(r'^$', views.show, name='show'),                 # 一覧
        url(r'^(?P<id>\d+)/$', views.detail, name='detail'), # 詳細
        url(r'^new/$', views.edit, name='new'),              # 追加
        url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),# 修正
        url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),  # 削除
        url(r'^search/$', views.search, name='search'),        # 検索
        url(r'^mypage/$', views.mypage, name='mypage'),   # マイページ
        url(r'^taskadd/(?P<id>\d+)/$', views.taskadd, name='taskadd'),# タスク追加
        url(r'^taskedit/(?P<id>\d+)/$', views.taskedit, name='taskedit'),# タスク修正
        url(r'^make/(?P<id>\d+)/$', views.make, name='make'),#
)