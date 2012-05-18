# -.- coding:utf8 -.-
from main.models import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from main.forms import UserCreateForm, LoginForm, EditProfileForm, TweetForm
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf


def home(request):
    return render_to_response('home.html')


def done(request):
    return render_to_response('login.html')


def registro(request):
    form = UserCreateForm
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    return render_to_response('registro.html', {
        'form': form,
    }, RequestContext(request))


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                users = authenticate(username=username, password=password)
                if users is not None:
                        login(request, users)
                        return redirect('profile', username)
                else:
                    try:
                        username = User.objects.get(email=username).username
                        users = authenticate(username=username, password=password)
                        if users is not None:
                            login(request, users)
                            return redirect('profile', username)
                    except:
                        pass
        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        dic = {'form': form}
        dic.update(csrf(request))
        return render_to_response('login.html', dic)


def log_out(request):
    logout(request)
    return redirect('home')


def edit_profile(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
            if form.is_valid():
                form.save()
                user = UserProfile.objects.get(user=request.user)
                return redirect('profile', username=user.user.username)
            else:
                return render_to_response('registro.html', {'form': form, }, RequestContext(request))
        form = EditProfileForm(instance=UserProfile.objects.get(user=request.user))
        dic = {'form': form}
        dic.update(csrf(request))
        return render_to_response('edit_profile.html', dic)
    return redirect('login')


def show_user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(user=user)
        dic = {'user': userprofile, 'followers': len(userprofile.followers()), 'followings': len(userprofile.followings()), }
        dic.update({'tweets': userprofile.tweet_set.all()})
        if request.user.is_authenticated:
            loged_profile = UserProfile.objects.get(user=request.user)
            dic.update({'follow':  userprofile in loged_profile.followings()})
            dic.update({'it_self': request.user == user})
        return render_to_response('profile.html', dic)
    except Exception, e:
        print e
        return redirect('done')


def view_tweet(request, id):
    tweet = Tweet.objects.get(pk=id)
    dic = {'tweet': tweet}
    return render_to_response('tweet.html', dic)


def follow_user(request, id):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        user = UserProfile.objects.get(pk=id)
        userprofile.follow(user)
        return redirect('profile', username=user.user.username)


def unfollow_user(request, id):
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
        user = UserProfile.objects.get(pk=id)
        userprofile.unfollow(user)
        return redirect('profile', username=user.user.username)


def add_tweet(request):
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            user = UserProfile.objects.get(user=request.user)
            user.tweet(status)
            return redirect('profile', username=user.user.username)
    return render_to_response('add_tweet.html', {
        'form': form,
        }, RequestContext(request))


def feed(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        dic = {'tweets': user.feed()}
        return render_to_response('timeline.html', dic)


def edit_tweet(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    form = TweetForm(instance=tweet)
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            user = UserProfile.objects.get(user=request.user)
            return redirect('profile', username=user.user.username)
    return render_to_response('add_tweet.html', {
        'form': form,
        }, RequestContext(request))


def delete_tweet(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    tweet.delete()
    user = UserProfile.objects.get(user=request.user)
    return redirect('profile', username=user.user.username)
