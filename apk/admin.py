from django.contrib import admin
from multiprocessing import Process

from sign.models import Sign
from utils.apk_sign import make_sign,commpress_apk,apk_sign
# Register your models here.
from apk.models import Apk, Temp, CpApk
from django.utils.html import format_html
import os
import time
from CreateApk.settings import HOST


def logic_delte(modeladmin, request, queryset):
    queryset.update(isdelete=1)

logic_delte.short_description = '逻辑删除'

class ApkAdmin(admin.ModelAdmin):
    list_display = ['create', 'id','apk_name', 'app_name', 'Edition', 'apk_file', 'cpUser', 'sign', 'update', 'load_sign_apk']
    fieldsets = [(None, {'fields': ['apk_name','app_name', 'Edition', 'apk_file']}),  # 显示
                 # ('选择渠道和签名', {'fields': ['sign', 'channel'], 'classes': ['collapse']}),  # 隐藏
                 ]
    list_per_page = 30  # 分页条数
    list_filter = ('create', 'apk_name', 'app_name')  # 过滤器
    search_fields = ('create', 'apk_name', 'app_name')  # 搜索
    # list_display_links = ['id']
    list_editable = ('id',)
    readonly_fields = ['id']
    actions = [logic_delte]


    def get_queryset(self, request):
        qs = super(ApkAdmin, self).get_queryset(request)
        return qs.filter(isdelete=0)

    #  配置 只读字段
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields if f.name == 'isdelete']
    # 自定义保存
    def save_model(self, request, obj, form, change):
        # 自定义操作

        obj.cpUser = request.user.username
        obj.save()
    # 自定义跳转页面
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     print('2222')
    #     result_template = super(ApkAdmin, self).change_view(request, object_id, form_url, extra_context)
    #     result_template['location'] = '/admin/apk/apk/'
    #     return result_template

    # def add_view(self, request, form_url='', extra_context=None):
    #     result_template = super(ApkAdmin, self).changeform_view(request, None, form_url, extra_context)
    #     result_template['location'] = '/admin/apk/apk/'
    #     return result_template


# 注销硬删除
admin.site.disable_action('delete_selected')
admin.site.register(Apk, ApkAdmin)


class TempAdmin(admin.ModelAdmin):
    list_display = ['channel']
    fieldsets = [(None, {'fields': ['channel']}),  # 显示
                 ('选择签名', {'fields': ['sign'], 'classes': ['collapse']}),
                 ('新增签名', {'fields': ['Password', 'Alias', 'Confirm', 'First_and_LastName', 'OrganizationalUnit', 'Organization', 'City_or_Locality', 'State_or_Province', 'Country_Code'], 'classes': ['collapse']}),  # 隐藏
                 ]

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.sign:
            apk = Apk.objects.get(id=int(request.GET.get('id')))
            apk_name = apk.apk_name
            apk.channel = obj.channel
            apk.sign = obj.sign

            # 找到apk包，签名文件
            apk_path = request.GET.get('path')
            sign_path = './media{}'.format(apk.sign.path)
            # 生成压缩包
            commpress_apk(apk_path)
            # time.sleep(2)
            # 生成签名文件
            apk_sign(sign_path, apk_name)
            apk.save()

        else:
            apk = Apk.objects.get(id=int(request.GET.get('id')))
            apk_name = apk.apk_name

            rsa_name = request.POST.get('Alias')
            name = request.POST.get('First_and_LastName')
            password = request.POST.get('Password')
            commpany = request.POST.get('OrganizationalUnit')
            organization = request.POST.get('Organization')
            city = request.POST.get('City_or_Locality')
            province = request.POST.get('State_or_Province')
            country = request.POST.get('Country_Code')

            # 生成签名
            make_sign(rsa_name,password,name,commpany,organization,city,province,country)
            # 找到 apk包 压缩apk
            apk_path = request.GET.get('path')
            commpress_apk(apk_path)
            # time.sleep(2)
            # 对apk添加签名
            # 签名文件路径
            sign_path = './media/sign/{}.jks'.format(rsa_name)
            apk_sign(sign_path,apk_name)
            sign = Sign.objects.create(sign_code=obj.Alias + 'jks', path='/sign/{}.jks'.format(rsa_name), sing_akp=rsa_name)
            apk = Apk.objects.get(id=int(request.GET.get('id')))
            apk.channel = obj.channel
            apk.sign = sign
            apk.save()


    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def add_view(self, request, form_url='', extra_context=None):
        result_template = super(TempAdmin, self).changeform_view(request, None, form_url, extra_context)
        result_template['location'] = '/admin/apk/apk/'
        return result_template

admin.site.register(Temp, TempAdmin)



class CpApkAdmin(admin.ModelAdmin):
    list_display = ['create', 'id', 'apk_name', 'app_name', 'Edition', 'apk_file']

    fieldsets = [(None, {'fields': ['apk_name', 'app_name', 'Edition', 'apk_file']}),  # 显示
                 # ('选择渠道和签名', {'fields': ['sign', 'channel'], 'classes': ['collapse']}),  # 隐藏
                 ]
    list_per_page = 30  # 分页条数
    list_filter = ('create', 'apk_name', 'app_name')  # 过滤器
    search_fields = ('create', 'apk_name', 'app_name')  # 搜索

    list_display_links = ['apk_file']
    readonly_fields = []

    def save_model(self, request, obj, form, change):
        # 自定义操作

        obj.cpUser = request.user.username
        obj.save()

    def get_queryset(self, request):
        qs = super(CpApkAdmin, self).get_queryset(request)
        return qs.filter(isdelete=0, cpUser=request.user.username)

admin.site.register(CpApk, CpApkAdmin)


