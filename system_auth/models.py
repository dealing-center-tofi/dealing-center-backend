from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class SystemUserManager(UserManager):
    def get_queryset(self):
        return SystemUserQuerySet(self.model)


class SystemUserQuerySet(models.QuerySet):
    pass


class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)

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
