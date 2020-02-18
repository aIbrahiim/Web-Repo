from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    gender_CHOICES = [
        ('M','Male'),
        ('F','Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=1,
        choices = gender_CHOICES,
        default = 'M'
        )
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    weight = models.SmallIntegerField(
        default = 10,
        validators = [MaxValueValidator(300),MinValueValidator(10)]
    )
    height = models.SmallIntegerField(
        default = 10,
        validators = [MaxValueValidator(300),MinValueValidator(10)]
    )
    smoking = models.BooleanField(default = False)
    birthdate = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)
    @receiver(post_save,sender = User)
    def create_user_profile(sender, instance,created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance,created, **kwargs):
        instance.profile.save()
