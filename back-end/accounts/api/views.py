from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework import permissions  
from rest_framework import viewsets
import base64
import tempfile
from accounts.models import Profile
from .app_settings import (
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    

)

from django.core import serializers
from django.http import HttpResponse
from django.core.files.base import ContentFile
import cv2
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

#end
User = get_user_model()

from .serializers import(
    UserCreateSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    UserDetailsSerializer,
)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()   
  

class UploadProfilePictureView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
  
    def post(self, request, *args, **kwargs):
        cur_user = User._default_manager.get(username=request.user)
        profile = Profile.objects.filter(user=cur_user)[0]
        profile.profile_picture =  request.data.get('profile_picture')
        profile.save()
        return Response(
            {"detail": _("Profile Picture has been updated.")},
            status=status.HTTP_200_OK
        )

class UploadProfilePictureAndroidView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
  
    def post(self, request, *args, **kwargs):
        img64 = str(request.data['profile_picture'])
        print(img64)
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
        cur_user = User._default_manager.get(username=request.user)
        profile = Profile.objects.filter(user=cur_user)[0]
        profile.profile_picture = img
        profile.save()
        return Response(
                {"detail": _("Profile Picture has been updated.")},
                status=status.HTTP_200_OK
            )
"""
class UploadProfilePictureAndroidView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
  
    def post(self, request, *args, **kwargs):
        profile_picture = request.data['profile_picture']
        fh = tempfile.NamedTemporaryFile(delete=False)
        extension =  profile_picture.name.split(".")[1]
        filename = "{}.{}".format(fh.name,extension)
        print(fh, extension, filename)
        
        cur_user = User._default_manager.get(username=request.user)
        profile = Profile.objects.filter(user=cur_user)[0]
        profile.profile_picture = profile_picture 
        profile.save()
        return Response(
            {"detail": _("Profile Picture has been updated.")},
            status=status.HTTP_200_OK
        )
        
  """      
    
class EmailTokenObtainPairView(TokenObtainPairView):
    queryset=User.objects.all()
    serializer_class = CustomTokenObtainPairSerializer


 master
class UserDetailsView(RetrieveAPIView):

=======
 master
    def get(self, request, *args, **kwargs):
        ser = UserDetailsSerializer(request.user)
        return Response(ser.data)
    
class PasswordResetView(GenericAPIView):
   
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
  
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )


class PasswordChangeView(GenericAPIView):

    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})
