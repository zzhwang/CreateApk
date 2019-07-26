from django.contrib import admin

# Register your models here.
from sign.models import Sign


class SignAdmin(admin.ModelAdmin):
    list_display = ['sign_code', "path"]

    # def save_model(self, request, obj, form, change):
    #     pass

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


# admin.site.register(Sign, SignAdmin)