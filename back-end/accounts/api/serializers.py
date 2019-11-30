from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.response import Response

from rest_framework.serializers import (
    CharField,
    EmailField,
    
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from accounts.models import Profile
from django.contrib.auth.models import User


Users = get_user_model()

#SignUp Stuff
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'phone',
            'gender',
            'country',
            'city',
            'weight',
            'height',
            'smoking',
            'birthdate'
        ]




class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    profile = ProfileSerializer()
    confPassword = CharField()
    class Meta:
        model = Users
        fields = [
            'email',
            'password',
            'confPassword',
            'username',
            'profile'
        ]
        extra_kwayrgs = {
            "password":{"write_only":True},
            #"confPassword":{"write_only":True}
        }

    def perform_create(self, serializer):
        return {serializer.save(user=self.request.user)}

    def create(self, validated_data):
        #user = validated_data['user']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        profile = validated_data['profile']
        user_obj = Users(
            username = username,
            email = email
        )
        
        user_obj.set_password(password)
        user_obj.save()
        #set profile data
        new_user = Users.objects.get(email=email)
        new_user.profile.phone = profile["phone"]
        new_user.profile.gender = profile["gender"]
        new_user.profile.country = profile["country"]
        new_user.profile.city = profile["city"]
        new_user.profile.weight = profile["weight"]
        new_user.profile.height = profile["height"]
        new_user.profile.smoking = profile["smoking"]
        new_user.profile.age = profile["birthdate"]
        new_user.save()

        token = get_tokens_for_user(new_user)
        validated_data["token"] = token
        print(validated_data)
        return validated_data

    def validate_email(self, value):
        data = self.get_initial()
        email = value
        user_qs = Users.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This email has already registered")
        return value

    def validate_password(self, value):
        data = self.get_initial()
        confpassword = data.get("confPassword")
        password = value
        if password != confpassword:
            raise ValidationError("Password must match.")
        return value

    def validate_confPassword(self, value):
        data = self.get_initial()
        password = data.get("password")
        confPassword = value
        if password != confPassword:
            raise ValidationError("Password must match")
        return value



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Login stuff
class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        
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
