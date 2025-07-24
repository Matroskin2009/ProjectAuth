from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    number_phone = models.CharField(max_length=11, blank=True, null=True)
    ref_code = models.CharField(max_length=6, blank=True, null=True)

class InviteActivation(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inviter")
    invited = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invited")
