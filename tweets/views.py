from django.db.models import Q
from tweets.profiles.models import Profiles
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views import View
from .mixins import authenticatedorNot, ownerOrNot, loginreq
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import TweetForm
from.models import Tweet
# Create your views here.

User = get_user_model()


class searchView(View):
    def get(self, request, *args, **kwargs):
        req = request.GET.get("q")
        tweets = Tweet.objects.filter(content__icontains=req)
        users = User.objects.filter(username__icontains=req)
        context = {
            "tweets": tweets,
            "users": users
        }
        return render(request, "tweets/search.html", context)


class likeTweet(View):
    def get(self, request, *args, **kwargs):
        getTweet = get_object_or_404(Tweet, id=self.kwargs["id"])
        # print(getTweet)
        CurrentUser = get_object_or_404(User, username=request.user.username)
        # print(CurrentUser)
        fetchLikes = getTweet.likes.all()
        # print(fetchLikes)
        if CurrentUser in fetchLikes:
            getTweet.likes.remove(CurrentUser)
            getTweet.is_liked = False
            getTweet.save()
        else:
            getTweet.likes.add(CurrentUser)
            # print(getTweet.likes.all())
            getTweet.is_liked = True
            getTweet.save()
            # print(getTweet.likes.all())
        return redirect("profiles:UserDetail", username=request.user.username)


class Retweet(View):
    def get(self, request, *args, **kwargs):
        # print("i am inside")
        getTweet = get_object_or_404(Tweet, id=self.kwargs["id"])
        print(getTweet.parent)
        if getTweet.parent:
            pass
        else:
            Retweet = Tweet.objects.create(
                parent=getTweet, user=request.user, content=getTweet.content)
        # print(Retweet)
        return redirect("listtweet")


class TweetDetail(DetailView):

    def get_queryset(self, *args, **kwargs):
        query = Tweet.objects.all()  # we can get whatever queryset here just an example
        return query

    def get_object(self, *args, **kwargs):
        obj = self.get_queryset()
        qs = obj.get(id=self.kwargs["pk"])
        return qs


class updateTweet(ownerOrNot, UpdateView):
    form_class = TweetForm
    model = Tweet
    # if we dont use this template name it is going to render the create form omly
    template_name = "tweets/update.html"


class TweetDelete(DeleteView):
    model = Tweet
    pk_url_kwarg = "del"
    success_url = reverse_lazy("tweets:list-rest")


class CreateTweet(CreateView):
    form_class = TweetForm
    model = Tweet
    success_url = reverse_lazy("tweets:List")

    def form_valid(self, form):
        # equals to instance=form.save(commit=false)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Yeah its invalid form")
        # handle whatever you need to handlle
        print(form.errors)
        return super().form_invalid(form)


class ListTweet(loginreq, authenticatedorNot, ListView):

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q", None)
        print(query)
        if query is not None:
            qs = Tweet.objects.filter(content__icontains=query)
        else:
            qs = Tweet.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        Myuser = self.request.user
        followingme = Myuser.profile.followDetails.all().exclude(
            username=self.request.user.username)
        recomm = Profiles.objects.allinone()
        print("inside")
        print(recomm)
        recomm = recomm.exclude(
            Q(userprofile=self.request.user) | Q(userprofile__in=followingme))[:5]
        print(recomm)
        context = super().get_context_data(**kwargs)
        context["form"] = TweetForm()
        context["recommended"] = recomm
        context["create_url"] = reverse("tweets:Create")
        return context
