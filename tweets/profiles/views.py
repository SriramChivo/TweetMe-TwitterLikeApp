from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from .models import Profiles
User = get_user_model()


class UserDetail(DetailView):
    queryset = User.objects.all()
    template_name = "tweets/User_detail.html"

    def get_object(self, *args, **kwargs):
        userobject = User.objects.get(
            username__iexact=self.kwargs["username"])
        return userobject

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        get_kwargs = self.kwargs["username"]
        get_profile = get_object_or_404(User, username=get_kwargs)
        final = Profiles.objects.Followdetails(self.request.user, get_profile)
        if final is not None:
            if final:
                context["followdetail"] = "UnFollow"
            else:
                context["followdetail"] = "Follow"
        else:
            context["followdetail"] = None

        # myprofile = User.objects.get(username=self.request.user.username)
        # FollowingorNot = myprofile.profile.followDetails.all()
        # if self.request.user != get_profile:
        #     if get_profile in FollowingorNot:
        #         context["followdetail"] = "UnFollow"
        #     else:
        #         context["followdetail"] = "Follow"
        # else:
        #     context["followdetail"] = None
        return context


class FollowView(View):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     user = get_object_or_404(User, username=request.user.username)
        #     togglefollow = user.profile.followDetails.all()
        toFollow = self.kwargs.get("username", None)
        userobj, created = User.objects.get_or_create(username=toFollow)
        follow = Profiles.objects.togglefollow(request.user, userobj)
        #     if userobj in togglefollow:
        #         user.profile.followDetails.remove(userobj)
        #     else:
        #         user.profile.followDetails.add(userobj)
        return redirect("profiles:UserDetail", username=toFollow)
