from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from .serializers import FileSerializer
from keras.models import load_model
from sklearn.externals import joblib
from .apps import ImagedetectionConfig
import json
import os
import cv2
import pandas as pd
from keras import backend as K
from rest_framework import permissions
import base64
from django.core.files.base import ContentFile
from media.app import mediaConfig

mapper = joblib.load('current_model_mapping.pkl')
mapper = {v:k for k,v in mapper.items()}

class FileView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  parser_classes = (MultiPartParser, FormParser)
  
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    
    
    projectPath = os.path.dirname(__file__) #get the current directory of the project

    model = load_model('current_model.h5')

    mapper = joblib.load('current_model_mapping.pkl')
    
    mapper = {v:k for k,v in mapper.items()}
    
    def get_pred_class_name(pred_class_number):
      global mapper
      return mapper[pred_class_number]

    if file_serializer.is_valid():
      file_serializer.save()
      print(file_serializer.data['file'])
      imgPathList = str(file_serializer.data['file']).split('/')
      
      imgPath = mediaConfig.projectPath
      #print(imgPath)
      
      for p in imgPathList:
        if p == 'media':
          continue
        if p != '':
          imgPath = os.path.join(imgPath,p)
          #print(imgPath)
      

      #imgPath = os.path.join(file_serializer.data['file'])
      print(imgPath)
      img = cv2.imread(imgPath)
     
      pic = preprocess_single_image(img)
      pred_class = model.predict_classes(pic)[0]
      pred_class_name = get_pred_class_name(pred_class)

      
      ans = "Predicted is {}".format(pred_class_name.replace("%20"," "))
      os.remove(imgPath)
      return JsonResponse({'ans':ans}, safe=False)
    else:
      return JsonResponse("error", safe=False)


class FileViewAndroid(APIView):
  #permission_classes = [permissions.IsAuthenticated]

  #parser_classes = (MultiPartParser, FormParser)
  
  def post(self, request, *args, **kwargs):
    #file_serializer = FileSerializer(data=request.data)
    
    
    projectPath = os.path.dirname(__file__) #get the current directory of the project

    model = load_model('current_model.h5')

    mapper = joblib.load('current_model_mapping.pkl')
    
    mapper = {v:k for k,v in mapper.items()}
    
    def get_pred_class_name(pred_class_number):
      global mapper
      return mapper[pred_class_number]

    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    img64 = str(body_data['img'])
    format, imgstr = img64.split(';base64,')
    print("format", format)
    ext = format.split('/')[-1]

    data = base64.b64decode(imgstr) 
    file_name = "myphoto." + ext
    path = 'media/'+file_name
    newFile = open(path,'wb')
    newFile.write(data)
    newFile.close()
    img = cv2.imread(path)
    pic = preprocess_single_image(img)
    pred_class = model.predict_classes(pic)[0]
    pred_class_name = get_pred_class_name(pred_class)

    if pred_class_name is not None:
      ans = "Predicted is {}".format(pred_class_name.replace("%20"," "))
      os.remove(os.path.join(mediaConfig.projectPath,file_name))
      return JsonResponse({'ans':ans}, safe=False)
    else:
      return JsonResponse("error", safe=False)
 

    




def preprocess_single_image(pic):
  pic = cv2.resize(pic, (120,120))
    
  pic = pic.astype('float32')
    
  pic /= 255
    
    
  pic = pic.reshape(-1,120,120,3)
    
  return pic



"""
def get_pred_class_name(pred_class_number):
    global m
    m = ImagedetectionConfig.mapper
    return m[pred_class_number]
"""    
