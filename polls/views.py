from django.views.generic import DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from polls.models import Choice, Poll, Vote


template_set=getattr(settings, 'POLLS_TEMPLATE_SET', 'basic')
if not template_set=='basic':
    POLLS_TEMPLATES_PATH=template_set+'/'
else:
    POLLS_TEMPLATES_PATH=''

class PollListView(ListView):
    model = Poll
    template_name='polls/'+POLLS_TEMPLATES_PATH+'poll_list.html'


class PollDetailView(DetailView):
    model = Poll
    template_name='polls/'+POLLS_TEMPLATES_PATH+'poll_detail.html'
    
    def get_queryset(self):
        qs=Poll.objects.filter(id=self.kwargs['pk'])
        self.choices=Choice.objects.filter(poll=qs[0]).prefetch_related('votes__user')
        total_votes=0
        for choice in self.choices:
            total_votes+=len(choice.votes.all())
        self.total_votes=total_votes
        return qs

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        #~ check if the user has a right to vote
        can_vote = True
        has_voted = False
        if not self.request.user.is_anonymous():
            for choice in self.choices:
                for vote in choice.votes.all():
                    if self.request.user==vote.user:
                        can_vote = False
                        has_voted=True
                        break
        else:
            can_vote = False
        context['login_url'] = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        context['poll'].votable = can_vote
        context['choices'] = self.choices
        context['has_voted'] = has_voted
        context['total_votes'] = self.total_votes
        return context


class PollVoteView(RedirectView):
    
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        #~ control if user can vote
        can_vote=True
        if user.is_anonymous():
            can_vote=False
        for vote in Vote.objects.filter(poll=poll):
            if user==vote.user:
                can_vote=False
                break
        if can_vote:
            Vote.objects.create(poll=poll, user=user, choice=choice)
            messages.success(request, _("Thanks for your vote."))
        else:
            messages.warning(request, _("You can not vote."))
        return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:detail', args=[kwargs['pk']])
