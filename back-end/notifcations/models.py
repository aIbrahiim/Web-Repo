from django.contrib.auth.models import User
from django.db import models

import datetime

"""
This file use to describe all realted attrubutes to 
Tabib notification System

Notification body Consists of:
1-Name
2-message
3-release time

"""

class Notification(models.Model):

    #realted user-->(Foreign Key)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #Notification body
    name = models.CharField(max_length=20)
    message = models.CharField(max_length=100)
    time = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)

    