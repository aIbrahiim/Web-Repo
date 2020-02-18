from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
 

from .views import(
    UserCreateAPIView,
    EmailTokenObtainPairView
)

urlpatterns = [
    path('register/',UserCreateAPIView.as_view(),name='register'),
    path('login/',EmailTokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('refresh/',jwt_views.TokenRefreshView.as_view(),name ='refresh')

]
