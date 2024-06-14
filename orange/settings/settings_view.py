# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader,Context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orange.models import PublicItem,MyItem
import ast
import time
import math
import datetime

@login_required
def manage_vm_page(request):

    if request.method == "GET":
        username = request.session.get("username")
        return render(request, 'settings/my_vm.html')



@login_required
def public_parameter(request):
    username = request.session.get("username")

    context = {}
    dict_all_datable_data = {}

    obj_parameter = PublicItem.objects.all()
    for item in obj_parameter:
        dict_all_datable_data.update({item.item_name: item.item_value})

    context['data_package'] = dict_all_datable_data


    if request.method == "GET":
        return render(request, 'settings/public_parameter.html',context)

    elif request.method == "POST":
        para_name = request.POST['para_name'].strip()
        para_value = request.POST['para_value'].strip()
        action = int(request.POST['action'])

        if action == 1:
            try:
                pp = PublicItem.objects.get(item_name=para_name)
            except:
                new_para=PublicItem(item_name=para_name.upper(),item_value=para_value)
                new_para.save()
                result = "Add new parameter successfully!"
            else:
                pp.item_value = para_value
                pp.save()
                result = "Change new parameter successfully!"

            return HttpResponse(result)

        else:
            try:
                pp = PublicItem.objects.get(item_name=para_name)
            except:
                result = "No such parameter!"
            else:
                pp.delete()
                result = "Parameter delete successfully!"

            return HttpResponse(result)



@login_required
def my_parameter(request):
    username = request.session.get("username")
    context = {}
    if request.method == "GET":
        dict_all_datable_data = {}
        try:
            obj_parameter = MyItem.objects.filter(owner=username)
            for item in obj_parameter:
                dict_all_datable_data.update({item.item_name: item.item_value})
        except:
            dict_all_datable_data={}

        context['data_package'] = dict_all_datable_data
        return render(request, 'settings/my_parameter.html',context)

    elif request.method == "POST":
        para_name = request.POST['para_name'].strip().upper()
        para_value = request.POST['para_value'].strip()
        action = int(request.POST['action'])

        if action == 1:
            try:
                pp=MyItem.objects.get(owner=username, item_name=para_name)
                print(pp)
            except:
                new_para=MyItem(owner=username,item_name=para_name,item_value=para_value)
                new_para.save()
                result = "Add new parameter successfully!"
            else:
                pp.item_value = para_value
                pp.save()
                result = "Change new parameter successfully!"

            return HttpResponse(result)

        else:
            try:
                pp = MyItem.objects.get(item_name=para_name,owner=username)
            except:
                result = "No such parameter!"
            else:
                pp.delete()
                result = "Parameter delete successfully!"

            return HttpResponse(result)
        

@login_required
def jenkins_token(request):
    username = request.session.get("username")

    context = {}
    dict_all_datable_data = {}

    try:
        obj_parameter = MyItem.objects.get(owner=username)
    except:
        dict_all_datable_data.update({'Empty': 'Empty'})
    else:
        # for item in obj_parameter:
        dict_all_datable_data.update({obj_parameter.user_name: obj_parameter.item_value})

    context['data_package'] = dict_all_datable_data
    if request.method == "GET":
        return render(request, 'settings/jenkins_token.html',context)

    elif request.method == "POST":
        jenkins_user_name = request.POST['user_name'].strip()
        para_value = request.POST['para_value'].strip()

        try:
            pp = MyItem.objects.get(owner=username)
        except:
            new_para=MyItem(owner=username,user_name=jenkins_user_name ,item_value=para_value)
            new_para.save()
            result = "Add new token successfully!"
        else:
            pp.item_value = para_value
            pp.user_name = jenkins_user_name
            pp.save()
            result = "Change new token successfully!"

        return HttpResponse(result)

