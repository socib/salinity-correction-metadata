# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class AuditBaseModel(models.Model):
    """Model base amb auditoria"""

    created_on = models.DateTimeField(_(u'date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False,
                                   related_name='created_%(app_label)s_%(class)s',
                                   verbose_name=_('created by'))
    updated_on = models.DateTimeField(_(u'date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False,
                                   related_name='updated_%(app_label)s_%(class)s',
                                   verbose_name=_(u'updated by'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.created_by:
            self.created_by = user
        return super(AuditBaseModel, self).save(*args, **kwargs)
