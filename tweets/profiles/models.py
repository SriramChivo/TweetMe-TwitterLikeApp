from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db.models.signals import post_save
user = get_user_model()


class ProfileQueryset(models.Manager):
    use_for_related_fields = True

    def all(self):
        print(self.get_queryset())
        print(self.get_queryset().all())
        # print(self.instance)
        qs = self.get_queryset().all()
        # print(dir(self))
        get = qs.exclude(userprofile=self.instance)
        print(get)
        return get

    def allinone(self):
        qs = self.get_queryset().all()
        return qs

    def togglefollow(self, userobj, to_follow):
        Myprofile = get_object_or_404(user, username=userobj.username)
        getFollowDetails = Myprofile.profile.followDetails.all()
        if to_follow in getFollowDetails:
            Myprofile.profile.followDetails.remove(to_follow)
            return True
        else:
            Myprofile.profile.followDetails.add(to_follow)
            return False

    def Followdetails(self, userobj, checkdetail):
        myprofile = user.objects.get(username=userobj.username)
        FollowingorNot = myprofile.profile.followDetails.all()
        if userobj != checkdetail:
            if checkdetail in FollowingorNot:
                checked = True
            else:
                checked = False
        else:
            checked = None
        return checked


class Checking(models.Model):
    name = models.CharField(max_length=120, null=True)
    User = models.ForeignKey(user, on_delete=models.CASCADE)


class Profiles(models.Model):
    # if two or more fileds sharing one model then definetely
    # we need to mention related name because does'nt know which reverse match it has to do
    # example if you give user.profiles_set.all() because of userobject shared by two fields
    # it doesnot know which field it needs reverse macth
    userprofile = models.OneToOneField(
        user, on_delete=models.CASCADE, related_name="profile")
    followDetails = models.ManyToManyField(user, related_name="followed_By")

    def get_following(self):
        qs = self.followDetails.all().exclude(username=self.userprofile.username)
        return qs

    def get_follow_url(self):
        return reverse_lazy("profiles:Followview", kwargs={"username": self.userprofile.username})

    objects = ProfileQueryset()

    class Meta:
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.userprofile.username


def userprofilereceiver(sender, instance, created, *args, **kwargs):
    print(instance)
    Profiles.objects.get_or_create(userprofile=instance)


post_save.connect(userprofilereceiver, sender=user)
