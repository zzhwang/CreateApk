from django.contrib import admin

# Register your models here.
from channel.models import Channel


def logic_delte(modeladmin, request, queryset):
    queryset.update(isdelete=1)

logic_delte.short_description = '逻辑删除'
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channelName', 'channelNumber', "comName"]
    actions = [logic_delte]

    fieldsets = [(None, {'fields': ['channelName', 'channelNumber', "comName"]}),  # 显示
                 # ('选择渠道和签名', {'fields': ['sign', 'channel'], 'classes': ['collapse']}),  # 隐藏
                 ]
    def get_queryset(self, request):
        qs = super(ChannelAdmin, self).get_queryset(request)
        return qs.filter(isdelete=0)

admin.site.register(Channel, ChannelAdmin)