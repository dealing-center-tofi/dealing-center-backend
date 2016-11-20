from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SystemUser


class SystemUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets[:1] + (
        ('Personal info',
         {'fields':
              ('first_name', 'second_name', 'last_name', 'birth_date', 'email', 'answer_secret_question')
          }
         ),
    ) + UserAdmin.fieldsets[2:]


admin.site.register(SystemUser, SystemUserAdmin)
