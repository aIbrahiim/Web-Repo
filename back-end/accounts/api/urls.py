from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from django.contrib.auth import views as auth_views

from .views import(
    UserCreateAPIView,
    EmailTokenObtainPairView,
    PasswordResetConfirmView,
    PasswordResetView,
    PasswordChangeView,
 )


urlpatterns = [
    path('register/',UserCreateAPIView.as_view(),name='register'),
    path('login/',EmailTokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('refresh/',jwt_views.TokenRefreshView.as_view(),name ='refresh'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

   
]