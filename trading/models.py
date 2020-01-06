from django.db import models
from accounts.models import Profile
# Create your models here.


class Cards(models.Model):
    name = models.CharField(max_length=30)
    village = models.CharField(max_length=30)
    level = models.IntegerField(default=10)
    maxLevel = models.IntegerField(default=10)
    heroes = models.BooleanField()
    xp = models.IntegerField(default=40)
    type = models.CharField(max_length=30, default='troops')
    card_images = models.ImageField(upload_to='card_images/', null=True)

    def __str__(self):
        return f'{self.name}'


class DeckUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class DeckCard(models.Model):
    quantity = models.IntegerField()
    cards = models.ForeignKey(Cards, on_delete=models.CASCADE)
    deck = models.ForeignKey(DeckUser, on_delete=models.CASCADE)


class Transactions(models.Model):
    receiver = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, default=None, related_name='receiver', null=True)
    sender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='sender')
    status = models.CharField(max_length=10)
    card_sent = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='card_sent')
    card_received = models.ForeignKey(Cards, on_delete=models.DO_NOTHING, default=None, related_name='card_received', null=True)
    price = models.IntegerField(default=None, null=True)

    def __str__(self):
        return f'{self.sender}'


