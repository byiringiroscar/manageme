from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL


# Create your models here.


class Test(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='image')
