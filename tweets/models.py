from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save
from tags.signals import tag_dynamic
# from tags.models import Tags
# Create your models here.
usermodel = get_user_model()


def Retweet(self):
    print(self.model())
    return ""


class Tweet(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(usermodel, on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=140)
    likes = models.ManyToManyField(
        usermodel, null=True, blank=True, related_name="likes")
    is_liked = models.BooleanField(null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:100]

    def get_absolute_url(self):
        return reverse("tweets:Detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("tweets:Update", kwargs={"pk": self.pk})

    def get_likes(self):
        # print(obj)
        # print(self.likes.all())
        likeCount = self.likes.all().count()
        # print(likeCount)
        return likeCount

    class Meta:

        verbose_name_plural = "Tweets"
        ordering = ["-updated"]


def TweetReceiver(sender, instance, created, *args, **kwargs):
    import re
    if created:
        regex = r'#(?P<user>\w+)'
        taglist = re.findall(regex, instance.content)
        print(taglist)
        print(instance.__class__)  # <class 'tweets.models.Tweet'>
        tag_dynamic.send(sender=instance.__class__, hash_dynamics=taglist)


post_save.connect(TweetReceiver, sender=Tweet)
