from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    USER = (
        ('1', 'Admin'),
        ('2', 'Cook'),
        ('3', 'Waiter'),
    )

    user_type = models.CharField(max_length=200, choices=USER, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

    def __str__(self):
        return self.user_type
