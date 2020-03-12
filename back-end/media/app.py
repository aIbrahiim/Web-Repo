from django.apps import AppConfig
import os

class mediaConfig(AppConfig):
    name = 'media'
    projectPath = os.path.dirname(__file__)


