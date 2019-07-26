from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# class UserProfile(AbstractUser):
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=u"修改时间", blank=True)
#     createTime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间', blank=True, null=True)
#     # objects = UserManager()
#
#     class Meta:
#         db_table = 'users'
#         verbose_name = "用户信息"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.username