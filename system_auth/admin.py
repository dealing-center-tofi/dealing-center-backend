from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SystemUser


class SystemUserAdmin(UserAdmin):
    pass


admin.site.register(SystemUser, SystemUserAdmin)
