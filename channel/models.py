from django.db import models

# Create your models here.
class Channel(models.Model):
    channelName = models.CharField(max_length=100, verbose_name='渠道名', null=True, blank=True)
    channelNumber = models.CharField(max_length=100, verbose_name='渠道号', null=True, blank=True)
    comName = models.CharField(max_length=100, verbose_name='公司名', null=True, blank=True)
    isdelete = models.IntegerField(default=0)

    class Meta:
        db_table = 'channel'
        verbose_name = '渠道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.channelName