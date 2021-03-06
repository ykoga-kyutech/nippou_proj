"""nippou_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = [

    # ルート
    url(r'^', include('nippou_app.urls', namespace='nippou_app')),

    # 管理画面
    url(r'^admin/', include(admin.site.urls)),

    # アプリ関係
    url(r'^nippou_app/', include('nippou_app.urls', namespace='nippou_app')),

    # ログイン関係 -> nippou_app側に持っていきたい
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'nippou_app/login.html'}, name='login' ),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'nippou_app/logout.html'}, name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
