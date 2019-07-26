from django.contrib import admin

# from user.models import UserProfile
from django.contrib import admin


# Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username']
#     actions = ['delete_selected']

# admin.site.register(UserProfile, UserAdmin)

admin.site.site_header = '出包后台'
admin.site.site_title = '出包'