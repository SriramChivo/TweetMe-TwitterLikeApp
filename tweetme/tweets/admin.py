from django.contrib import admin
from .models import Tweet
from .forms import TweetForm
# Register your models here.
from tweets.profiles.models import Profiles, Checking

admin.site.register(Profiles)
admin.site.register(Checking)


class TweetAdmin(admin.ModelAdmin):
    # form = TweetForm
    model = Tweet
    readonly_fields = ["created", "updated"]
    fields = ["parent", "user", "content",
              "created", "updated", "likes", "is_liked", "is_reply"]
    search_fields = ["content"]
    list_display = ["content"]


admin.site.register(Tweet, TweetAdmin)
