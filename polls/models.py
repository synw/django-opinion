# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Poll(models.Model):
    question = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)

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
    poll = models.ForeignKey(Poll, null=True, related_name='choices')
    choice = models.CharField(null=True, max_length=255)

    def count_votes(self):
        return self.votes.count()

    def __unicode__(self):
        return self.choice

    class Meta:
        ordering = ['choice']


class Vote(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    poll = models.ForeignKey(Poll, null=True)
    choice = models.ForeignKey(Choice, null=True, related_name='votes')

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

    class Meta:
        unique_together = (('user', 'poll'))
