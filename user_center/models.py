from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=40, null=False)
    mail = models.CharField(max_length=20, null=False)
    verifivation = models.BooleanField(default=False)
