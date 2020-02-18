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


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    
    """
    projectPath = os.path.dirname(__file__) #get the current directory of the project

    modelPath = os.path.join(projectPath,'saved_models','current_model.h5' )
    model = load_model(modelPath)

    mapperPath = os.path.join(projectPath,'saved_models','current_model_mapping.pkl')
    mapper = joblib.load(mapperPath)
    
    mapper = {v:k for k,v in mapper.items()}
    """

    if file_serializer.is_valid():
      file_serializer.save()
      imgPathList = str(file_serializer.data['file']).split('/')
      imgPath = ImagedetectionConfig.projectPath
      for p in imgPathList:
        if p != '':
          imgPath = os.path.join(imgPath,p)
          #print(imgPath)
      
      #print(imgPath)
      
      img = cv2.imread(imgPath)
      
      #print(img)
      #print(imgPath)
      
      
      pic = preprocess_single_image(img)
      #print(ImagedetectionConfig.model)
      modelPath = os.path.join(ImagedetectionConfig.projectPath,'saved_models','current_model.h5' )
      model = load_model(modelPath)
      K.clear_session()
      pred_class = model.predict_classes(pic)
      K.clear_session()
      """
      pred_class_name = get_pred_class_name(pred_class)
      """

      return Response(file_serializer.data['file'], status=status.HTTP_201_CREATED)
      #return JsonResponse(file_serializer, safe=False)
    else:
      return JsonResponse("zezo", safe=False)


def preprocess_single_image(pic):
    
    
    
    pic = cv2.resize(pic, (120,120))
    
    pic = pic.astype('float32')
    
    pic /= 255
    
    
    pic = pic.reshape(-1,120,120,3)
    #print(pic)
    """
    """
    return pic


    
def get_pred_class_name(pred_class_number):
    global m
    m = ImagedetectionConfig.mapper
    return m[pred_class_number]