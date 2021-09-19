from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Tweet, Hashtag, Person
import re
from django.http import HttpResponseRedirect
# Create your views here.
def splash(request):
    return render(request, 'splash.html', {})

def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            content = request.POST['content']
            newTweet = Tweet.objects.create(author=request.user, content=content)
            hashtags = re.findall(r"#(\w+)", content)
            for hashtag in hashtags:
                newHashtag = Hashtag(tag=hashtag)
                newHashtag.save()
                newTweet.hashtag.add(newHashtag)
        tweets = Tweet.objects.order_by('-timestamp')
        return render(request, 'home.html', {"tweets":tweets, 'following': Person.objects.get(name=request.user).following.all()})
    else:
        return redirect("/login")
    
def login_view(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('/login?error=failure')
        
        login(request, user)
        return redirect('/home')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username, password, email, bio = request.POST['username'], request.POST['password'], request.POST['email'], request.POST['bio']
        user = User.objects.create_user(username=username, password=password, email=email)
        newBio = Person.objects.create(name=user, bio=bio)
        login(request, user)
        return redirect('/home')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

def profile(request):
    if request.user.is_authenticated:
        requestPerson = Person.objects.get(name = request.user)
        profile = User.objects.get(username=request.GET['user'])
        profilePerson = Person.objects.get(name = profile)
        tweets = Tweet.objects.filter(author=profile)
        followerNum = Person.objects.get(name=profile).followerNum
        followers = Person.objects.get(name=profile).followers.all()
        following = Person.objects.get(name=profile).following.all()
        followingNum = Person.objects.get(name=profile).followingNum
        userBio = Person.objects.get(name=profile).bio
        return render(request, 'profile.html', {'tweets':tweets, 'name':profile.username, 'profile':profile, 'followerNum': followerNum, 'userBio':userBio, 'following':following, 'followers':followers, 'followingNum':followingNum, 'profilePerson': profilePerson, 'requestPerson': requestPerson})
    else:
        return redirect("/login")

def delete(request):
    tweet = Tweet.objects.get(id=request.GET['id'])
    tweet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def hashtag_view(request):
    hashtag = request.GET['hashtag']
    hashtags = Hashtag.objects.filter(tag=hashtag)
    tweets = Tweet.objects.filter(hashtag__in=hashtags)
    return render(request, 'hashtag.html', {'tweets':tweets, 'hashtag':hashtag})

def like_tweet(request):
    tweet = Tweet.objects.get(id=request.GET['id'])
    if request.user not in tweet.tweet_likes.all():
        tweet.likes += 1
        tweet.tweet_likes.add(request.user)
        tweet.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_person(request):
    person = Person.objects.get(name = User.objects.get(username=request.GET['user']))
    if request.user not in person.followers.all():
        person.followerNum += 1
        person.followers.add(request.user)
        other = Person.objects.get(name = request.user)
        other.following.add(person.name)
        other.followingNum += 1
        other.save()
        person.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfollow_person(request):
    person = Person.objects.get(name = User.objects.get(username=request.GET['user']))
    if request.user in person.followers.all():
        person.followerNum -= 1
        person.followers.remove(request.user)
        person.save()
        other = Person.objects.get(name = request.user)
        other.following.remove(person.name)
        other.followingNum -= 1
        other.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def dislike_tweet(request):
    tweet = Tweet.objects.get(id=request.GET['id'])
    tweet.likes -= 1
    tweet.tweet_likes.remove(request.user)
    tweet.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def updateBio(request):
    person = Person.objects.get(name=request.user)
    person.bio = request.POST['newbio']
    person.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))