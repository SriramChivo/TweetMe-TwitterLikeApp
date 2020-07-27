from django.urls import path, re_path
from .views import UserDetail, FollowView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

app_name = 'profiles'


urlpatterns = [

    re_path(r"^(?P<username>[\w0-9@. ]+)/$",
            UserDetail.as_view(), name="UserDetail"),
    re_path(r"^(?P<username>[\w0-9@. ]+)/follow/$",
            FollowView.as_view(), name="Followview"),

]
