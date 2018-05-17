from django.db import models
from ..LoginReg.models import User


# Create your models here.


class FriendManager(models.Manager):
    def create_friend(self, user_id, friend_id):
        newfriend = self.create(
            user_id=user_id,
            friend_id=friend_id,
        )
        newfriend2 = self.create(
            user_id=friend_id,
            friend_id=user_id,
        )
        return newfriend

    def delete_friend(self, user_id, friend_id):
        delete = Friend.objects.get(user_id=user_id, friend_id=friend_id).delete()
        delete2 = Friend.objects.get(user_id=friend_id, friend_id=user_id).delete()
        return delete


class Friend(models.Model):
    user_id = models.ForeignKey(User, related_name="user")
    friend_id = models.ForeignKey(User, related_name="friend")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = FriendManager()
