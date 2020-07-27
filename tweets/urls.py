from django.urls import path, re_path
from .views import CreateTweet, TweetDetail, ListTweet, updateTweet, TweetDelete, Retweet, likeTweet, searchView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

app_name = 'tweets'


urlpatterns = [

    path("", CreateTweet.as_view(), name="Create"),
    path("search/", searchView.as_view(), name="search"),
    path("mytweets/", TemplateView.as_view(template_name="tweets/mytweets.html"),
         name="mytweets"),
    path("all/", RedirectView.as_view(url=reverse_lazy("listtweet")),
         name="list-rest"),
    # path("all/", ListTweet.as_view(), name="List"),
    re_path(r"^(?P<pk>\d+)/$", TweetDetail.as_view(), name="Detail"),
    re_path(r"^(?P<pk>\d+)/update/$", updateTweet.as_view(), name="Update"),
    re_path(r"^(?P<del>\d+)/delete/$", TweetDelete.as_view(), name="Delete"),
    re_path(r"^(?P<id>\d+)/retweet/$", Retweet.as_view(), name="retweet"),
    re_path(r"^(?P<id>\d+)/like/$", likeTweet.as_view(), name="like"),

]
