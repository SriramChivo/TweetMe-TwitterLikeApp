from django.db import models
from tweets.models import Tweet
from .signals import tag_dynamic
# Create your models here.


class Tags(models.Model):
    tags = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tags

    def get_tweets(self):
        return Tweet.objects.filter(content__icontains="#"+str(self.tags))


def tagReceiver(sender, hash_dynamics, *args, **kwargs):
    if hash_dynamics:
        for hash in hash_dynamics:
            getobj = Tags.objects.get(tags=hash)
            if getobj:
                pass
            else:
                Tags.objects.create(tags=hash)


tag_dynamic.connect(tagReceiver)
