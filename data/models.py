from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# Create your models here.
# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(models.Model):
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=10, null=False)


class Blog(models.Model):
    title = models.CharField(max_length=50, null=False)
    body = models.TextField()
    # 博客的创建者
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.title


