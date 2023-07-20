from django.contrib import admin
from user.models import CustomUser
from user.views import GetUserView


class USerAdminView(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, USerAdminView)
