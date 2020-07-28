from django.urls import path, re_path
from .views import ListTweetApi, CreateTweet, RetweetAPI, LikeApi, ProfileAPI, RetreiveTweet, hashtagsApi, mytweets, DeleteOrUpdate

app_name = 'api'


urlpatterns = [

    path("list/", ListTweetApi.as_view(), name="ListApi"),
    path("mytweets/", mytweets.as_view(), name="mytweets"),
    path("create/", CreateTweet.as_view(), name="createapi"),
    path("list/view/", ProfileAPI.as_view(), name="listview"),
    re_path(r"^(?P<id>\d+)/retweet/$",
            RetweetAPI.as_view(), name="retweetapi"),
    re_path(r"^(?P<id>\d+)/delete/$",
            DeleteOrUpdate.as_view(), name="deleteapi"),
    re_path(r"^tags/(?P<tags>\w+)/$",
            hashtagsApi.as_view(), name="hashtagsApi"),
    re_path(r"^(?P<id>\d+)/like/$",
            LikeApi.as_view(), name="likeapi"),
    re_path(r"^profiles/(?P<username>[\w0-9@. ]+)/$",
            ProfileAPI.as_view(), name="ProfileAPI"),
    re_path(r"^Details/(?P<pk>\d+)/tweet/$",
            RetreiveTweet.as_view(), name="Retreive"),

]
