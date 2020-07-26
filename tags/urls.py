from django.urls import path, re_path
from .views import TagPage
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

app_name = 'tags'


urlpatterns = [

    re_path(r"^tags/(?P<tags>\w+)/$", TagPage.as_view(), name="tagsview"),

]
