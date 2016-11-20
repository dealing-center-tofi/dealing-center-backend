from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


def generate():
    return str(uuid.uuid4())[:50]


class SystemUserManager(UserManager):
    def get_queryset(self):
        return SystemUserQuerySet(self.model)


class SystemUserQuerySet(models.QuerySet):
    pass


class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, default=generate)
    email = models.EmailField(max_length=100, unique=True)

    first_name = models.CharField(_('first name'), max_length=30)
    second_name = models.CharField(_('second name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30)

    birth_date = models.DateField(null=True)
    answer_secret_question = models.CharField(max_length=30, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = SystemUserManager()

    class Meta:
        verbose_name = _('system user')
        verbose_name_plural = _('system users')

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
