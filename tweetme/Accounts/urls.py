from django.urls import path, re_path
from .views import registration, loginTweet
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

app_name = 'accounts'


urlpatterns = [
    path("register/", registration.as_view(), name="registration"),
    path("login/", loginTweet.as_view(), name="login"),
]
