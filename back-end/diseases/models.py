from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class Diseases(models.Model):
    diseaseName = models.TextField(unique=True, max_length=250)


class OldDiseases(models.Model):
    treatment = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases,on_delete=models.CASCADE)

class NewDiseases(models.Model):
    treatment = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases,on_delete=models.CASCADE)
    time = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)

class DiseasesSymptoms(models.Model):
    symptoms = models.TextField(unique=True, max_length=250)
    disease = models.ForeignKey(Diseases,on_delete=models.CASCADE)



class Organs(models.Model):
    organName = models.TextField(unique=True, max_length=250)
    disease = models.ManyToManyField(Diseases)

class HumanSystems(models.Model):
    systemName = models.TextField(unique=True, max_length=250)
    disease = models.ManyToManyField(Organs)
