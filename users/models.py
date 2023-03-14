from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    chat_group = models.ManyToManyField(to="chat.ChatGroup", related_name="profiles")
