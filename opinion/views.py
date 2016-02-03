# -*- coding: utf-8 -*-

import importlib
from django.views.generic import DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from opinion.models import Choice, Poll, Vote


#~ select the template se to use
template_set=getattr(settings, 'POLLS_TEMPLATE_SET', 'bootstrap')
if not template_set=='bootstrap':
    POLLS_TEMPLATES_PATH=template_set+'/'
else:
    POLLS_TEMPLATES_PATH=''

#~ optional extra permission check if a user can vote
#~ set POLLS_CUSTOM_PERMS_MANAGER='app.module.function' to define the 
#~ path to your custom check function
custom_perm_check=getattr(settings, 'POLLS_CUSTOM_PERMS_MANAGER', None)
if custom_perm_check:
    function_string = custom_perm_check
    mod_name, func_name = function_string.rsplit('.',1)
    mod = importlib.import_module(mod_name)
    custom_perm_check = getattr(mod, func_name)

class PollListView(ListView):
    model = Poll
    template_name='opinion/'+POLLS_TEMPLATES_PATH+'poll_list.html'
    context_object_name = 'polls'


class PollDetailView(DetailView):
    model = Poll
    #template_name='opinion/'+POLLS_TEMPLATES_PATH+'poll_vote.html'
    
    def get_queryset(self):
        qs=Poll.objects.filter(id=self.kwargs['pk'])
        self.poll = qs[0]
        self.choices=Choice.objects.filter(poll=self.poll).prefetch_related('votes__user')
        total_votes=0
        for choice in self.choices:
            total_votes+=len(choice.votes.all())
        self.total_votes=total_votes
        #~ check if the user has a right to vote
        self.can_vote = True
        self.has_voted = False
        if not self.request.user.is_anonymous():
            for choice in self.choices:
                for vote in choice.votes.all():
                    if self.request.user==vote.user:
                        self.can_vote = False
                        self.has_voted=True
                        break
        else:
            self.can_vote = False
        #~ debug cheat
        """
        if settings.DEBUG:
            if self.request.user.is_superuser:
                self.can_vote = True
        """
        return qs
    
    def get_template_names(self):
        #~ use the show results template if the user can not vote
        names=['opinion/'+POLLS_TEMPLATES_PATH+'poll_vote.html']
        if not self.can_vote:
            names=['opinion/'+POLLS_TEMPLATES_PATH+'poll_results.html']
        return names

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['login_url'] = getattr(settings, 'LOGIN_URL', '/login/')
        context['choices'] = self.choices
        context['has_voted'] = self.has_voted
        context['can_vote'] = self.can_vote
        context['total_votes'] = self.total_votes
        return context
    

class PollResultsView(DetailView):
    model = Poll
    template_name='opinion/'+POLLS_TEMPLATES_PATH+'poll_results.html'
    context_object_name ='poll'
    def get_queryset(self):
        qs=Poll.objects.filter(id=self.kwargs['pk'])
        self.poll = qs[0]
        self.choices=Choice.objects.filter(poll=self.poll).prefetch_related('votes__user')
        total_votes=0
        for choice in self.choices:
            total_votes+=len(choice.votes.all())
        self.total_votes=total_votes
        #~ check if the user has a right to vote
        self.can_vote = True
        self.has_voted = False
        if not self.request.user.is_anonymous():
            for choice in self.choices:
                for vote in choice.votes.all():
                    if self.request.user==vote.user:
                        self.can_vote = False
                        self.has_voted=True
                        break
        else:
            self.can_vote = False
        #~ debug cheat
        """
        if settings.DEBUG:
            if self.request.user.is_superuser:
                self.can_vote = True
        """
        return qs

    def get_context_data(self, **kwargs):
        context = super(PollResultsView, self).get_context_data(**kwargs)
        context['login_url'] = getattr(settings, 'LOGIN_URL', '/login/')
        context['choices'] = self.choices
        context['has_voted'] = self.has_voted
        context['can_vote'] = self.can_vote
        context['total_votes'] = self.total_votes
        return context


class PollVoteView(RedirectView):
    permanent = True
    
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        if not request.POST.has_key('choice_pk'):
            messages.warning(request,_('Thank you to select an answer for your vote'))
            return redirect('opinion:detail', pk=poll.pk)
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        #~ control if user can vote
        can_vote=True
        if user.is_anonymous():
            can_vote=False
        for vote in Vote.objects.filter(poll=poll):
            if user==vote.user:
                can_vote=False
                break
        #~ if an extra function is provided to check if user can vote, then use it
        #~ this function must return a boolean
        if not self.request.user.is_anonymous() and can_vote and custom_perm_check:
            can_vote=custom_perm_check(self.request)
        if can_vote:
            Vote.objects.create(poll=poll, user=user, choice=choice)
            messages.success(request, _("Thanks for your vote."))
        else:
            messages.warning(request, _("You can not vote."))
        return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('opinion:detail', args=[kwargs['pk']])
