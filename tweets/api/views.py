from .serializers import TweetSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from tweets.models import Tweet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from tags.models import Tags

User = get_user_model()


class DeleteOrUpdate(APIView):
    def get(self, *args, **kwargs):
        kw = self.kwargs.get("id", None)
        getobj = Tweet.objects.get(id=kw)
        if(getobj.user == self.request.user):
            getobj.delete()
            return Response({"Message": "Deleted"}, status=200)
        else:
            return Response({"Message": "Not a Owner to delete this post"})


class mytweets(ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.filter(user=self.request.user)
        return qs


class hashtagsApi(ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self, *args, **kwargs):
        org = self.kwargs["tags"]
        print(org)
        kw = self.request.GET.get("q", None)
        if kw is not None and kw != "":
            qs = Tweet.objects.filter(content__icontains=kw)
        else:
            qs = Tweet.objects.filter(content__icontains="#"+str(org))
            print(qs)
        return qs


class ProfileAPI(ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self, *args, **kwargs):
        kw = self.request.GET.get("q", None)
        if("view" in self.request.get_full_path()):
            return Tweet.objects.filter(content__icontains=kw)
        if kw is None or kw != "":
            qs = Tweet.objects.filter(
                Q(user__username=self.kwargs["username"]) & Q(
                    content__icontains=kw))
        else:
            qs = Tweet.objects.filter(user__username=self.kwargs["username"])
        return qs


class LikeApi(APIView):

    def get(self, request, *args, **kwargs):
        getTweet = get_object_or_404(Tweet, id=self.kwargs["id"])
        # print(getTweet)
        CurrentUser = get_object_or_404(User, username=request.user.username)
        # print(CurrentUser)
        fetchLikes = getTweet.likes.all()
        # print(fetchLikes)
        if CurrentUser in fetchLikes:
            getTweet.likes.remove(CurrentUser)
            re = False
        else:
            getTweet.likes.add(CurrentUser)
            re = True
        return Response(re)


class RetweetAPI(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        et = Tweet.objects.get(id=id)
        print(et)
        print(et.parent)
        if et.parent:
            return Response("Not Allowed", status=400)
        else:
            # et.parent = et
            # et.save()
            newtweet = Tweet.objects.create(
                parent=et, user=request.user, content=et.content)
            ser = TweetSerializer(
                newtweet, context={"request": self.request}).data
            # we need to pass context manually here get_serializer_context() wont work becausewe are calling the serializers manually
            # get_serializer_context() will be called get_serialize_class() only not through get,post,put,delete manual https
            # 93 line will work because we are using to retreive tweets with drf method only not by manual so after qs drf will call both
            # get_serializer_class() and get_serializer_context() both automatically.

        return Response(ser)


class ListTweetApi(ListAPIView):

    serializer_class = TweetSerializer
    # queryset = Tweet.objects.all()
    # if we want request alone no need to use get_serializer_context()instead we can use self.context.get("request") automatically
    # because already get_serializer_context() called whe get_serializer_class() called with context "request"

    def get_serializer_context(self, *args, **kwargs):
        # print("inside context")
        context = super(ListTweetApi, self).get_serializer_context(
            *args, **kwargs)
        context["request"] = self.request
        # print("dfghjkl")
        # print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        # print(self.request.GET)
        kw = self.request.GET.get("q", None)
        # print(kw)

        if kw is None or kw != "":
            # print("following")
            qs = Tweet.objects.filter(content__icontains=kw)
            # following = self.request.user.profile.followDetails.all(
            # ).values_list("username", flat=True)
            # # print(following)
            # qs2 = Tweet.objects.filter(user=self.request.user)
            # qs1 = Tweet.objects.filter(user__username__in=following)
            # qs = (qs2 | qs1).distinct().order_by("-created")
            # cfe style #
            # or following = self.request.user.profile.followDetails.all() <queryset <user (chivo)>,<user sriram>>
            # Tweet.objects.filter(user__in=following)
            # print(final)
            # for i in following:
            #     print(i)
        else:
            following = self.request.user.profile.followDetails.all()
            # print(following)
            # following = following.values_list("username", flat=True)
            qs2 = Tweet.objects.filter(user=self.request.user)
            qs1 = Tweet.objects.filter(user__in=following)
            qs = (qs2 | qs1).distinct().order_by("-created")
            # qs = Tweet.objects.all()
        return qs


class CreateTweet(CreateAPIView):

    serializer_class = TweetSerializer
    # permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        # print(self.request.user)
        serializer.save(user=self.request.user)


class RetreiveTweet(ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self, *args, **kwargs):
        kw = self.kwargs["pk"]
        # print("yessss")
        # qs = get_object_or_404(Tweet, id=kw)
        qs1 = Tweet.objects.filter(id=kw)
        # print(qs)
        # print(qs.count())
        # print(g)
        if qs1.exists() and qs1.count() == 1:
            qs11 = qs1.first()
            # print(qs1)
            if not qs11.parent:
                # print("yessss")
                qs2 = Tweet.objects.filter(parent=qs11)
                # print(qs2)
                qs = (qs1 | qs2).distinct().order_by("-id")
            else:
                c = qs11.parent.id
                qs1 = Tweet.objects.filter(id=kw)
                qs2 = Tweet.objects.filter(id=c)
                qs = (qs1 | qs2).distinct().order_by("-id")
        return qs
