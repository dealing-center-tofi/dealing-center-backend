from __future__ import unicode_literals

from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    def __unicode__(self):
        return '%s : %s' % (self.name, self.value)
