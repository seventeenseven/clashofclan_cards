from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    PROFILE_CHOICES = (
        (50, 'Barbarian King'),
        (40, 'Archer Queen'),
        (30, 'Battle Machine'),
        (20, 'P.E.K.K.A'),
        (10, 'Healer')
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pictures/')
    personnage = models.IntegerField(choices=PROFILE_CHOICES, default=10)
    points = models.IntegerField(default=10)
    coins = models.IntegerField(default=200)

    def __str__(self):
        return f'{self.user}'
