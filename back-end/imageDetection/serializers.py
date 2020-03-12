from rest_framework import serializers
from .models import File
from rest_framework.serializers import (
  CharField
)

class FileSerializer(serializers.ModelSerializer):
  
  class Meta():
    model = File
    fields = ('file', 'remark', 'timestamp')


