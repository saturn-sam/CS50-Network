from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Post, Profile


def index(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["post"]
        date = datetime.now()
        if content != "":
            Post.objects.create(user = user, content = content, date = date)

    posts = Post.objects.all().order_by('-date') 
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })

def profile(request,username):
    if request.user.is_anonymous:
        target_user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=target_user).order_by('-id')
        follower = Profile.objects.filter(following=target_user)
        following = Profile.objects.filter(follower=target_user)
        totalfollower = len(follower)
        totalfollowing = len(following)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 
    
        context = {
            'posts': posts.count(),
            'target_user': target_user,
            'page_obj': page_obj,
            'follower': follower,
            'totalfollower': totalfollower,
            'following': following,
            'totalfollowing': totalfollowing

        }

        return render(request, "network/profile.html", context)       
    else: 
        if request.method == 'GET':
            
            target_user = get_object_or_404(User, username=username)
            posts = Post.objects.filter(user=target_user).order_by('-id')
            follower = Profile.objects.filter(following=target_user)
            following = Profile.objects.filter(follower=target_user)
            following_target_user = Profile.objects.filter(follower=request.user, following=target_user)
            totalfollower = len(follower)
            totalfollowing = len(following)
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'posts': posts.count(),
                'target_user': target_user,
                'page_obj': page_obj,
                'follower': follower,
                'totalfollower': totalfollower,
                'following': following,
                'totalfollowing': totalfollowing,
                'following_target_user': following_target_user
            }
            return render(request, "network/profile.html", context)
        else:
            target_user = get_object_or_404(User, username=username)
            following_target_user = Profile.objects.filter(following=target_user, follower=request.user)
            posts = Post.objects.filter(user=target_user).order_by('-id')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if not following_target_user:
                print(target_user)
                print(following_target_user)
                follow = Profile.objects.create(following=target_user, follower=request.user)
                follow.save()
                follower = Profile.objects.filter(following=target_user)
                following = Profile.objects.filter(follower=target_user)
                following_target_user = Profile.objects.filter(following=target_user, follower=request.user)
                print(following_target_user)
                total_follower = len(follower)
                total_following = len(following)
                context = {
                    'posts': posts.count(),
                    'target_user': target_user,
                    'page_obj': page_obj,
                    'follower': follower,
                    'following': following,
                    'totalfollowing': total_following,
                    'totalfollower': total_follower,
                    'following_target_user': following_target_user
                }
                return render(request, "network/profile.html", context)
            else:
                print(following_target_user)
                following_target_user.delete()
                follower = Profile.objects.filter(following=target_user)
                following = Profile.objects.filter(follower=target_user)
                totalfollower = len(follower)
                totalfollowing = len(following)
            context = {
                'posts': posts.count(),
                'target_user': target_user,
                'page_obj': page_obj,
                'follower': follower,
                'following': following,
                'totalfollowing': totalfollowing,
                'totalfollower': totalfollower,
                'following_target_user': following_target_user
            }
            return render(request, "network/profile.html", context)

def like_post(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            post_id = request.GET['post_id']
            isliked = Post.objects.get(pk=post_id)
            if request.user in isliked.liked.all():
                isliked.liked.remove(request.user)
            else:
                isliked.liked.add(request.user)
                isliked.save()
            return HttpResponse('Success')

def edit(request, id):
    if request.method == 'POST':
        post = Post.objects.get(pk=id)
        if request.user == post.user:
            post.content = request.POST["textarea"]
            post.save()
            return HttpResponse('success')
        else:
            return HttpResponse('You have no permission to edit the post!')
    else:
        return HttpResponse('Wrong route!!')


def following(request):
    if request.user.is_anonymous:
        return render(request, 'network/following.html')
    else:
        if request.method == 'GET':
            user = request.user
            following = Profile.objects.filter(follower=request.user).values('following_id')

            posts = Post.objects.filter(user__in=following).order_by('-id')
            print(posts)
            if not following:
                return render(request, 'network/following.html', {'message': "You are not following anybody."})
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'network/following.html',{'page_obj':page_obj})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
