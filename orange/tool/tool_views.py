
# encoding: utf-8

import copy
import datetime
import os
import sys

import json,requests,csv
from requests.auth import HTTPBasicAuth
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
from orange.common.log import Log
from orange.models import PublicItem,MyItem
from orange import settings
from mtell_automation import settings
from orange.tool import upload_result_to_vsts
log = Log()

# headers = {
#     "Accept": 'application/json;api-version=7.1-preview.2',
#     "Content-Type": "application/json",
# }


from django.http import FileResponse

def download(request):
    file = open(os.path.join(settings.BASE_DIR, 'static', 'file','temp', "template_upload.csv"), 'rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'  
    myname='template_upload.csv'
    response['Content-Disposition']='attachment;filename="{0}"'.format(myname)  
    return response

def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        import os
        f = open(os.path.join(settings.BASE_DIR, 'static', 'file', file_obj.name), 'wb')
        print(file_obj,type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('Uploaded!')


@login_required
def update_result_to_vsts(request):
    username = request.session.get("username")   
    if request.method == "GET":
        try:
            plan_id = MyItem.objects.get(item_name='PLAN_ID',owner=username).item_value
        except:
            plan_id = PublicItem.objects.get(item_name='PLAN_ID').item_value

        try:
            suite_id = MyItem.objects.get(item_name='SUITE_ID',owner=username).item_value
        except:
            suite_id = PublicItem.objects.get(item_name='SUITE_ID').item_value
        context={
            "plan_id":plan_id,
            "suite_id":suite_id,
            # "personal_access_token":personal_access_token
        }
        return render(request, 'tool/update_result_to_vsts.html',context)
    elif request.method == "POST":
        try:
            personal_access_token = MyItem.objects.get(item_name='PERSONAL_ACCESS_TOKEN',owner=username).item_value
        except:
            personal_access_token = PublicItem.objects.get(item_name='PERSONAL_ACCESS_TOKEN').item_value

        if request.POST['plan_id']:
            plan_id = str(request.POST['plan_id'])
        
        if request.POST['suite_id']:
            suite_id = str(request.POST['suite_id'])
       
        if request.POST['file_upload']:
            file_upload = str(request.POST['file_upload'])
        else:
            return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>File not uploaded!</b>")

        file_upload_new=file_upload.split("\\")[-1]
        cvs_file_name=os.path.join(settings.BASE_DIR, 'static', 'file', file_upload_new)

        url = 'https://aspentech-alm.visualstudio.com/AspenTech/_apis/testplan/Plans/' + plan_id + '/Suites/' + suite_id + '/TestPoint?includePointDetails=true&returnIdentityRef=true'

        try:
            all_data = upload_result_to_vsts.get_data_from_csv(cvs_file_name)
            log.info("Get data from " + cvs_file_name)
        except Exception as e:
            log.error(e)
            return HttpResponse("<b style='color: green; font-family: Arial, sans-serif;font-size:20px'>" + e + "</b>")
        
        test_points_id=upload_result_to_vsts.get_test_points_id(all_data,plan_id,suite_id,personal_access_token)
        if test_points_id:
            log.info("Begin to update result. ")
        else:
            return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>Test Case not found or Token is invalid!</b>")



        for item in test_points_id:
            for key,value in item.items():
                value=value.strip().lower()
                if value == 'passed':
                    state=2
                elif value == 'failed':
                    state=3
                elif value == 'active':
                    state=1
                else:
                    raise ValueError("Invalid input")
                data=[{
                        "id": key,
                        "results": {
                            "outcome": state

                    }
                }]
            try:
                response = requests.patch(url,json=data,headers=upload_result_to_vsts.headers,auth=HTTPBasicAuth('', personal_access_token))
            except Exception as e:
                if "Invalid URL" in str(e):
                    return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>URL is invalid!</b>")
                else:
                    log.error(e)
            # log.info(data)
            # log.info(response.status_code)
            # log.info(response.content)
        return HttpResponse("<b style='color: green; font-family: Arial, sans-serif;font-size:20px'>All results update successfully!</b>")



@login_required
def update_result_to_vsts_new(request):
    username = request.session.get("username")   
    if request.method == "GET":
        try:
            plan_id = MyItem.objects.get(item_name='PLAN_ID',owner=username).item_value
        except:
            plan_id = PublicItem.objects.get(item_name='PLAN_ID').item_value

        try:
            suite_id = MyItem.objects.get(item_name='SUITE_ID',owner=username).item_value
        except:
            suite_id = PublicItem.objects.get(item_name='SUITE_ID').item_value
        context={
            "plan_id":plan_id,
            "suite_id":suite_id,
            # "personal_access_token":personal_access_token
        }
        return render(request, 'tool/update_result_to_vsts.html',context)
    elif request.method == "POST":
        try:
            personal_access_token = MyItem.objects.get(item_name='PERSONAL_ACCESS_TOKEN',owner=username).item_value
        except:
            personal_access_token = PublicItem.objects.get(item_name='PERSONAL_ACCESS_TOKEN').item_value

        if request.POST['plan_id']:
            plan_id = str(request.POST['plan_id'])
        
        if request.POST['suite_id']:
            suite_id = str(request.POST['suite_id'])
       
        if request.POST['file_upload']:
            file_upload = str(request.POST['file_upload'])
        else:
            return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>File not uploaded!</b>")

        file_upload_new=file_upload.split("\\")[-1]
        cvs_file_name=os.path.join(settings.BASE_DIR, 'static', 'file', file_upload_new)

    
        try:
            all_data = upload_result_to_vsts.get_data_from_csv(cvs_file_name)
            log.info("Get data from " + cvs_file_name)
        except Exception as e:
            log.error(e)
            return HttpResponse("<b style='color: green; font-family: Arial, sans-serif;font-size:20px'>" + e + "</b>")
        
        test_points_id=upload_result_to_vsts.get_test_points_id_new(all_data,plan_id,suite_id,personal_access_token)
        if test_points_id:
            log.info("Begin to update result. ")
        else:
            return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>Test Case not found or Token is invalid!</b>")


        result=upload_result_to_vsts.create_run(test_points_id,plan_id,personal_access_token)

        if result:
            return HttpResponse("<b style='color: green; font-family: Arial, sans-serif;font-size:20px'>All results update successfully!</b>")
        else:
            return HttpResponse("<b style='color: red; font-family: Arial, sans-serif;font-size:20px'>URL is invalid!</b>")



