from django.apps import AppConfig
from keras.models import load_model
from sklearn.externals import joblib
import json
import os
import cv2
import pandas as pd

import os

class ImagedetectionConfig(AppConfig):
    name = 'imageDetection'
    projectPath = os.path.dirname(__file__)
    modelPath = os.path.join(projectPath,'saved_models','current_model.h5' )
    model = load_model(modelPath)

    mapperPath = os.path.join(projectPath,'saved_models','current_model_mapping.pkl')
    mapper = joblib.load(mapperPath)

    mapper = {v:k for k,v in mapper.items()}
