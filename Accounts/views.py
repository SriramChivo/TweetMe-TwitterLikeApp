from django.shortcuts import render
from .forms import tweetUserForm, loginForm
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
# Create your views here.


class logoutTweet(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse("accounts:login"))


class loginTweet(FormView):
    form_class = loginForm
    template_name = "Accounts/loginForm.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        auth = authenticate(username=username, password=password)
        print(auth)
        if auth:
            login(self.request, auth)
            return HttpResponseRedirect(reverse("tweets:list-rest"))
        else:
            print("Unauthenticate")
            form = loginForm()
            message = "Username or Password is Incorrect"
            return render(self.request, self.template_name, context={"message": message, "form": form})


class registration(CreateView):
    form_class = tweetUserForm
    template_name = "Accounts/Registration.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form1 = form.save(commit=False)
        sim = form.cleaned_data.get("username")
        form1.first_name = "Default"
        form1.save()
        print(sim)
        return super(registration, self).form_valid(form)


# class loginAuth(View):
#     def get(self, request, *args, **kwargs):
#         username = "Lubezki"
#         password = "Chivo@07"
#         auth = authenticate(username=username, password=password)
#         login(request, auth)
#         return HttpResponseRedirect(reverse("tweets:list-rest"))
