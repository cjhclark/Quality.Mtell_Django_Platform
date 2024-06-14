# -*- coding: utf-8 -*-
import copy
import datetime
import os
import sys

import json
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.db import connection
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader,Context


from django.shortcuts import render
def do_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/index')
        else:
            return render(request, 'login.html')

    errors= []
    account=None
    password=None
    if request.method == 'POST' :
        if not request.POST.get('username'):
            errors.append('Please input username！')
        else:
            account = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append('Please input password')
        else:
            password= request.POST.get('password')
        if account is not None and password is not None:
            user = authenticate(username=account,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    request.session['username'] = account
                    request.session.set_expiry(7200)
                    return HttpResponseRedirect('/index')
                else:
                    errors.append('User is not active!')
            else:
                errors.append('Username or Password error')
    return render(request,'login.html', {'errors': errors})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def index(request):
    context={}
    user_info={}
    username = request.session.get("username")
    user_type=request.user.is_staff
    user_info.update({'user': username})
    user_info.update({'user_type': user_type})

    context['user_info']=user_info

    if request.user.is_authenticated():
        return render(request, 'index.html',context)
    else:
        return render(request, 'index.html', context)


def register_success(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render(request, 'register_success.html')


def change_password(request):

    errors = []
    account = None
    old_password = None
    new_password1 = None
    new_password2 = None
    compare_flag = False

    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('Please input user name')
        else:
            account = request.POST.get('username')
        if not request.POST.get('old_password'):
            errors.append('Please input password')
        else:
            old_password = request.POST.get('old_password')
        if not request.POST.get('new_password1'):
            errors.append('Please input new password')
        else:
            new_password1 = request.POST.get('new_password1')
        if not request.POST.get('new_password2'):
            errors.append('Please repeat new password')
        else:
            new_password2 = request.POST.get('new_password2')

        if new_password1 is not None and new_password2 is not None:
            if new_password1 == new_password2:
                compare_flag = True
            else:
                errors.append('two new passwords are different')

        if account is not None and old_password is not None and new_password1 is not None and new_password2 is not None and compare_flag:
            user = authenticate(username=account, password=old_password)
            if user is not None:
                if user.is_active:
                    user.set_password(new_password1)
                    user.save()
                    return render(request, 'index.html',{'msg':1})
                else:
                    errors.append('User is inavtive')
            else:
                errors.append('Password is incorrect')  

    return render(request,'change_password.html', {'errors': errors})


def user_manage(request):
    user_info={}
    context={}
    result=''
    status=''
    if request.user.is_authenticated():
        if request.method == 'GET':
            if request.user.is_staff:
                username = request.session.get("username")
                action = request.GET.get('action')
                if action=='5':
                    status = request.GET.get('status')
                    if status=='Inactive':
                        obj_user = User.objects.filter(is_active=0)
                    elif status=='Active':
                        obj_user = User.objects.filter(is_active=1)
                    else:
                        obj_user = User.objects.all()
                else:
                    obj_user = User.objects.all()

                list_info=[]
                for item in obj_user:
                    temp_list=[]
                    temp_list.append(item.username)
                    temp_list.append(item.email)
                    temp_list.append(item.is_staff)
                    temp_list.append(item.is_active)
                    temp_list.append(item.date_joined)
                    temp_list.append(item.last_login)
                    list_info.append(temp_list)
                    user_info.update({'list_info':list_info})

                context['data_package'] = user_info
                return render(request,'user_manage.html',context)
        elif request.method == 'POST':
            action=request.POST['action']
            if action=='1':
                chg_user_name = request.POST['user_name']
                User.objects.filter(username=chg_user_name).update(is_active=1)
                result = "Activate successfully!"
            elif action=='2':
                chg_user_name = request.POST['user_name']
                User.objects.filter(username=chg_user_name).update(is_active=0)
                result = "Lock successfully!"
            elif action=='3':
                chg_user_name = request.POST['user_name']
                User.objects.filter(username=chg_user_name).update(is_staff=1)
                result = "Set as admin successfully!"
            elif action=='4':
                chg_user_name = request.POST['user_name']
                User.objects.filter(username=chg_user_name).delete()
                result = "Delete successfully!"
            elif action=='5':
                status = request.POST['status']
                User.objects.filter(username=status).delete()
                result = "Delete successfully!"
            return HttpResponse(result)
    else:
        return HttpResponseRedirect('/login/')


def manage_chg_pwd(request):
    errors = []
    new_password1 = None
    new_password2 = None
    compare_flag = False
    user_to_change=''
    if request.user.is_authenticated():
        if request.user.is_staff:
            if request.method == 'GET':
                user_to_change = request.GET.get('P')
                return render(request, 'manage_chg_pwd.html',{'user_to_change':user_to_change})
            elif request.method == 'POST':
                user_to_change = request.POST.get('username')
                if not request.POST.get('new_password1'):
                    errors.append('Please input new password')
                else:
                    new_password1 = request.POST.get('new_password1')
                if not request.POST.get('new_password2'):
                    errors.append('Please repeat new password')
                else:
                    new_password2 = request.POST.get('new_password2')

                if new_password1 is not None and new_password2 is not None:
                    if new_password1 == new_password2:
                        compare_flag = True
                    else:
                        errors.append('two new passwords are different')

                if new_password1 is not None and new_password2 is not None and compare_flag:
                    user = User.objects.get(username=user_to_change)
                    user.set_password(new_password1)
                    user.save()
                    return HttpResponseRedirect('/user_manage/')

            return render(request,'manage_chg_pwd.html', {'errors': errors,'user_to_change':user_to_change})

    else:
        return HttpResponseRedirect('/login/')

