from django.db import models

# Create your models here.
from django.utils.html import format_html

from CreateApk.settings import HOST
from channel.models import Channel
from sign.models import Sign


class Apk(models.Model):
    create = models.DateTimeField(verbose_name='创建时间', auto_now=True, null=True, blank=True)
    sign = models.ForeignKey(Sign, verbose_name='签名', null=True, blank=True)
    channel = models.ForeignKey(Channel, verbose_name='渠道', null=True, blank=True)
    apk_name = models.CharField(max_length=200, verbose_name='包名', null=True)
    app_name = models.CharField(max_length=200, verbose_name='应用名', null=True)
    Edition = models.CharField(max_length=200, verbose_name='版本号', null=True,help_text='同一个apk包版本号不能重复填写')
    apk_file = models.FileField(upload_to='apk/%Y/%m/%d/', verbose_name='APK包', null=True)
    cpUser = models.CharField(max_length=100, verbose_name='开发者', null=True, blank=True)
    isdelete = models.IntegerField(default=0)

    class Meta:
        db_table = 'apk'
        verbose_name = '生成签名'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ('view_apk', 'view_apk'),
        # )

    def __str__(self):
        return self.sign.sign_code if self.sign else ""

    def update(self):

        return format_html('<a href="/admin/apk/temp/add/?id={}&path={}">出包</a>'.format(self.id,self.apk_file.file))

    update.short_description = u'出包'

    def load_sign_apk(self):
        if not self.sign:
            return format_html('<p>未出包</p>')
        return format_html('<a href="/media/out/{}.apk">下载签名</a>'.format(self.apk_name))

    load_sign_apk.short_description = u'下载签名'




class Temp(models.Model):
    channel = models.ForeignKey(Channel, verbose_name='渠道', null=True, help_text='必填项')
    sign = models.ForeignKey(Sign, verbose_name='签名',unique=True, null=True, blank=True, help_text='如果选择了签名，就不能再给当包新增签名')
    Password = models.CharField(null=True, max_length=100, help_text='请输入6位以上', blank=True,)
    Alias = models.CharField(null=True, max_length=100, unique=True, blank=True, help_text='必填项')
    Confirm = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    First_and_LastName = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    OrganizationalUnit = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    Organization = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    City_or_Locality = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    State_or_Province = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')
    Country_Code = models.CharField(null=True, max_length=100, blank=True, help_text='必填项')

    class Meta:
        db_table = 'Temp'
        verbose_name = '临时表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Alias


class CpApk(Apk):
    class Meta:
        proxy=True
        verbose_name = u'添加apk'
        verbose_name_plural= u'添加apk'