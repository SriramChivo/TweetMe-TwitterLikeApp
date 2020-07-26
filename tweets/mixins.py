from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
user = get_user_model()


class authenticatedorNot(object):
    def dispatch(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            # print("yes")
            return super(authenticatedorNot, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Not Authenticated Please login and continue")


class loginreq(object):
    def dispatch(self, request, *args, **kwargs):
        if(request.user.is_authenticated):
            # print("yes")
            return super(authenticatedorNot, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse("accounts:login"))


class ownerOrNot(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # we need to call this object unless if you use self.object directly it will throw
        # 'tweetupdeview' object has no attribute 'object'
        if(obj.user == request.user):
            print("then its fine")
            return super(ownerOrNot, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Not a owner to edit this post sorry")
