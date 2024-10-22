from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联的用户', related_name='user_profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(blank=True, verbose_name='个人简介')

    # 你可以添加其他字段

    def __str__(self):
        return self.user.username
