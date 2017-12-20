from django.db import models


# Create your models here.
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
