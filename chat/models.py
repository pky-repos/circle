from django.db import models

from users.models import Profile


class ChatGroup(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Message(models.Model):
    chat_group = models.ForeignKey(to=ChatGroup, on_delete=models.CASCADE)
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="likes")



