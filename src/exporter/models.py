from __future__ import unicode_literals
from django.db import models


class ModelExport(models.Model):
    STATUS_CHOICES = (
        ('new', 'New',),
        ('processing', 'Processing',),
        ('failed', 'Failed',),
        ('success', 'Success',),
    )
    created_at = models.DateTimeField(verbose_name=u'created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'updated at', auto_now=True)

    user_id = models.CharField(verbose_name=u'user id', max_length=36)

    conditions = models.CharField(verbose_name=u'conditions', max_length=256)

    export_data = models.FileField(verbose_name=u'export data', upload_to='export/data/')
    export_file = models.FileField(verbose_name=u'export file', upload_to='export/files/')
    export_format = models.CharField(verbose_name=u'export format', max_length=8, default='json')

    status = models.CharField(verbose_name=u'export status', choices=STATUS_CHOICES, default='new', max_length=16)

    class Meta:
        verbose_name = u'model export'
        verbose_name_plural = u'model export'

        ordering = ['-created_at']
