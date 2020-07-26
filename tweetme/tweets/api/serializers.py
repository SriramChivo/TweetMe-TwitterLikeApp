from tweets.models import Tweet
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
from django.urls import reverse_lazy


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", 'url']

    def get_url(self, obj):
        url = reverse_lazy("profiles:UserDetail", kwargs={
                           "username": obj.username})
        return url


class ParentTweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    timesince = serializers.SerializerMethodField()
    retweetUrl = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ["id", "user", "content",
                  "created", "timesince", "retweetUrl"]

    def get_timesince(self, obj):
        return str(timesince(obj.created) + " ago")

    def get_retweetUrl(self, obj):
        return reverse_lazy("tweets:retweet", kwargs={"id": obj.id})


class TweetSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = UserSerializer(read_only=True)
    timesince = serializers.SerializerMethodField()
    is_retweet = serializers.SerializerMethodField()
    parent = ParentTweetSerializer(read_only=True)
    retweetUrl = serializers.SerializerMethodField()
    likecount = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ["id", "parent_id", "user", "content", "is_reply",
                  "created", "timesince", "parent", "is_retweet", "retweetUrl", "likecount", "is_liked"]

    def get_timesince(self, obj):
        return str(timesince(obj.created) + " ago")

    def get_is_retweet(self, obj):
        if obj.parent:
            return True
        return False

    def get_retweetUrl(self, obj):
        return reverse_lazy("tweets:retweet", kwargs={"id": obj.id})

    def get_likecount(self, obj):
        count = obj.likes.all().count()
        return count

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user
        # print(user)
        # print(obj.likes.all())
        if user in obj.likes.all():
            return True
        return False
