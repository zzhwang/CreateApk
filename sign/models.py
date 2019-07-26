from django.db import models

# Create your models here.


class Sign(models.Model):
    sign_code = models.CharField(max_length=100, verbose_name='签名码', null=True, blank=True)
    path = models.CharField(max_length=200, verbose_name='签名文件', null=True, blank=True)
    sing_akp = models.CharField(max_length=200, verbose_name='带签名的apk', null=True, blank=True)

    class Meta:
        db_table = 'sign'
        verbose_name = "签名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sign_code
