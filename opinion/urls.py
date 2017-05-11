from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from opinion.views import PollDetailView, PollListView, PollVoteView, PollResultsView


urlpatterns = [
    url(r'^$', PollListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/results/$', PollResultsView.as_view(), name='results'),
    url(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
]
