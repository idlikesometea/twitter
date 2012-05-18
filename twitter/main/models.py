from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, blank=True)
    profile_picture = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(null=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=140, blank=True)
    private = models.BooleanField()

    def follow(self, user):
        if user not in self.followings():
            Relationship.objects.create(follower=self, followed=user)

    def followers(self):
        return [relation.follower for relation in self.followers_relation.all()]

    def followings(self):
        return [relation.followed for relation in self.followings_relation.all()]

    def unfollow(self, user):
        if user in self.followings():
            Relationship.objects.filter(follower=self, followed=user).delete()

    def tweet(self, status):
        self.tweet_set.create(status=status)

    def feed(self):
        return Tweet.objects.filter(owner__in=self.followings() + [self])


class Tweet(models.Model):
    owner = models.ForeignKey(UserProfile)
    status = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class Relationship(models.Model):
    follower = models.ForeignKey(UserProfile, related_name="followings_relation")
    followed = models.ForeignKey(UserProfile, related_name="followers_relation")


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
