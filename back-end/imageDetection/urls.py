from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from .views import FileView,FileViewAndroid



urlpatterns = [
    path('',FileView.as_view(),name ='refresh'),
    path('android/',FileViewAndroid.as_view(),name ='refresh')

]
