from django.shortcuts import render
from .models import Tags
from django.views import View
# Create your views here.


class TagPage(View):
    def get(self, request, *args, **kwargs):
        context = {}
        tag, created = Tags.objects.get_or_create(tags=self.kwargs["tags"])
        context["tagobj"] = tag
        return render(request, "Tags/TagsView.html", context)
