from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    EmailField,
    ImageField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

from accounts.models import Profile

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError


"""
accounts serializer Consists of 3 parts
1- ProfileSerializer
2- UserCreateSerializer
3- LoginSerializer
"""



#get all users data
Users = get_user_model()


#SignUp Stuff
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'dateOfBirth',
            'gender',
            'phone',
            'city',
            'country',
            'height',
            'weight',
            'smoking',
            'profile_picture'
        ]




class UserCreateSerializer(ModelSerializer):
    profile = ProfileSerializer()
    conffPassword = CharField()
    name = CharField()
    class Meta:
        model = Users
        fields = [
            'email',
            'name',
            'password',
            'conffPassword',
            'profile',
             
         ]
        extra_kwayrgs = {
            "password":{"write_only":True},
            "conffPassword":{"write_only":True},            
        }

    def perform_create(self, serializer):
        return {serializer.save(user=self.request.user)}

    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        profile = validated_data['profile']

        user_obj = Users(
            username = email,
            email = email
        )

        nameList = name.split()
        if len(nameList) == 1:
            user_obj.first_name = name
        else :
            user_obj.first_name = nameList[0]
            user_obj.last_name = ' '.join(nameList[1:])

        user_obj.set_password(password)

        user_obj 

        user_obj.save()

        #set profile data
        new_user = Users.objects.get(email=email)
        print(new_user)
        print(profile)
        new_user.profile.dateOfBirth = profile["dateOfBirth"]
        new_user.profile.gender      = profile["gender"]
        new_user.profile.phone       = profile["phone"]
        new_user.profile.city        = profile["city"]
        new_user.profile.country     = profile["country"]
        new_user.profile.height      = profile["height"]
        new_user.profile. weight     = profile["weight"]
        new_user.profile.smoking     = profile["smoking"]
        new_user.profile.profile_picture  = profile["profile_picture"]
        new_user.save()

        token = get_tokens_for_user(new_user)
        """
        validated_data["token"] = token
        print(validated_data)
        """

        return validated_data

    #Validations
    def validate_email(self, value):
        data = self.get_initial()
        email = value
        user_qs = Users.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This email has already registered")
        return value

    def validate_password(self, value):
        data = self.get_initial()
        confpassword = data.get("conffPassword")
        password = value
        if password != confpassword:
            raise ValidationError("Password must match.")
        return value


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'dateOfBirth',
            'gender',
            'phone',
            'city',
            'country',
            'height',
            'weight',
            'smoking',
            'profile_picture',
        ]

#Login stuff
class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD
    def validate(self, attrs):
        #user_qs = Users.objects.filter(email=self.context.get('request').user)

        self.user = User.objects.filter(email=attrs[self.username_field]).first()
        if not self.user:
            raise ValidationError('The user is not valid.')
        
        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')
        

class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @classmethod
    def get_token(cls, user):
        token =  RefreshToken.for_user(user)
        return token
    
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        
        user = {} 
        user['name'] = self.user.username
        user['email'] = self.user.email
        data["User"] = user
        return data






class PasswordResetSerializer(serializers.Serializer):
   
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        return {}

    def validate_email(self, value):
        user_qs = Users.objects.filter(email=self.context.get('request').user)
        if not user_qs.exists():
            raise ValidationError("This email is not registered")
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
   
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass
    
    
    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        self._errors = {}
        print(attrs)
        try:
            
            self.user = Users._default_manager.get(username=user)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            raise ValidationError({'User': ['Not found']})

        self.custom_validation(attrs)
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
       
        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)


    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)










"""
from accounts.models import Profile
from django.contrib.auth.models import User
p = Profile(
    gender = 'M',
    country = 'Egypt',
    city = 'Alex',
    weight = 150,
    height = 120,
    smoking = False
)
u = User(
    username = 'abdo',
    email = 'speed@gmail.com',
    password = '123123',
    profiel = p
)
"""