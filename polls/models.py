# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name=_('Poll')
        verbose_name_plural = _('Polls')

    def count_choices(self):
        return self.choices.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choices.all():
            result += choice.count_votes()
        return result

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices')
    choice = models.CharField(max_length=255)

    def count_votes(self):
        return self.votes.count()

    def __unicode__(self):
        return self.choice

    class Meta:
        ordering = ['choice']
        verbose_name=_('Choice')
        verbose_name_plural = _('Choices')


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice, related_name='votes')

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

    class Meta:
        unique_together = (('user', 'poll'))
        verbose_name=_('Vote')
        verbose_name_plural = _('Votes')
