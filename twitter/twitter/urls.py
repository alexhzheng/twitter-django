"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import splash, login_view, home, logout_view, signup_view, profile, delete, hashtag_view, like_tweet, dislike_tweet, follow_person, unfollow_person, updateBio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash, name='splash'),
    path('login', login_view, name='login_view'),
    path('signup', signup_view, name='signup_view'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout_view'),
    path('profile/', profile, name='profile'),
    path('delete', delete, name='delete'),
    path('hashtag', hashtag_view, name='hashtag_view'),
    path('like_tweet', like_tweet, name='like_tweet'),
    path('follow_person', follow_person, name='follow_person'),
    path('unfollow_person', unfollow_person, name='unfollow_person'),
    path('dislike_tweet', dislike_tweet, name='dislike_tweet'),
    path('hashtag_view', hashtag_view, name='hashtag_view'),
    path('profile/updateBio', updateBio, name='updateBio'),
]
