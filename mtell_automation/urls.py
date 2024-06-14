"""mtell_automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from django.contrib import admin
from orange.user_management import user_views
from orange.tool import tool_views
from orange.settings import settings_view
from orange import views
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path(r'admin', admin.site.urls),
    re_path(r'^index', views.index),
    re_path(r'^tool/update_result_to_vsts$', tool_views.update_result_to_vsts),
    re_path(r'^tool/update_result_to_vsts_new', tool_views.update_result_to_vsts_new),

    re_path(r'^upload_ajax', tool_views.upload_ajax),
    re_path(r'^download', tool_views.download, name='file_down'),
    re_path(r'^login', views.do_login),
    re_path(r'^logout', views.logout),
    re_path(r'^register', views.register),
    re_path(r'^register_success', views.register_success),
    re_path(r'^change_password', views.change_password),
    re_path(r'^user_manage', views.user_manage),
    re_path(r'^manage_chg_pwd', views.manage_chg_pwd),
    re_path(r'^settings/manage_vm', settings_view.manage_vm_page),
    re_path(r'^settings/public_parameter', settings_view.public_parameter),
    re_path(r'^settings/my_parameter', settings_view.my_parameter),
    re_path(r'^settings/jenkins_token', settings_view.jenkins_token),


]
