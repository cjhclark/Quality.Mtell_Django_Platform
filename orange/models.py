# coding=utf-8
# models.py
from django.db import models  
  
class PublicItem(models.Model):  
    item_name = models.CharField(max_length=50, default='')  
    item_value = models.CharField(max_length=10000, default='')  
  
class MyItem(models.Model):  
    owner = models.CharField(max_length=60, default='')  
    item_name = models.CharField(max_length=50, default='')  
    item_value = models.CharField(max_length=10000, default='')
