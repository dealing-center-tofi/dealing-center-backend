from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SystemUser, SecretQuestion


class SystemUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets[:1] + (
        ('Personal info',
         {'fields':
             ('first_name', 'second_name', 'last_name', 'birth_date', 'email',
              'secret_question', 'answer_secret_question')
          }
         ),
    ) + UserAdmin.fieldsets[2:]


class SecretQuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(SystemUser, SystemUserAdmin)
admin.site.register(SecretQuestion, SecretQuestionAdmin)
