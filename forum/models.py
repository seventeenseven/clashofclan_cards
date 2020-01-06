from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Threads(models.Model):
    subject = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(default=timezone.now)


class Comments(models.Model):
    comment = models.TextField()
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(default=timezone.now)


class PrivateMessage(models.Model):
     sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
     receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
     msg_content = models.TextField()
     created_at = models.DateField(default=timezone.now)
     