from django.db import models
class File(models.Model):
  file = models.FileField(blank=False, null=False)
  remark = models.CharField(max_length=20,default="temp")
  timestamp = models.DateTimeField(auto_now_add=True)