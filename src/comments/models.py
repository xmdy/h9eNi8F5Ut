from __future__ import unicode_literals

from django.db import models

from common.helpers.postgresql.fields import LTreeField


class Comment(models.Model):
    created_at = models.DateTimeField(verbose_name=u'created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'updated at', auto_now=True)

    user_id = models.CharField(verbose_name=u'user id', max_length=36)

    object_type = models.CharField(verbose_name=u'object type', max_length=64)
    object_id = models.CharField(verbose_name=u'object id', max_length=36)

    parent = models.ForeignKey('Comment', blank=True, null=True, related_name=u'children')  # denormalization for comments management

    comment = models.TextField(verbose_name=u'comment')

    path = LTreeField(verbose_name=u'comment path')

    @property
    def level(self):
        return self.path.count('.')

    class Meta:
        verbose_name = u'comment'
        verbose_name_plural = u'comments'
        ordering = ['-parent_id', 'created_at']
