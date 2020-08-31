from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-time')
    return showposts(request, posts)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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

def viewuser(request, username):
    try:
        user = User.objects.get(username=username)
    except NameError:
        raise Http404
    posts = Post.objects.filter(posting_user=user).order_by('-time')
    return showposts(request, posts, True, user.username)


def showposts(request, posts, userpage=False, title='All Posts'):
    if posts.count() == 0 and not userpage:
        return render(request, "network/index.html", {
            'empty': True
        })
    paginator = Paginator(posts, 10)
    pagenum = request.GET.get('pagenum', 1)
    try: 
        pagenum = int(pagenum)
    except ValueError:
        raise Http404
    if pagenum in paginator.page_range:
        items = paginator.page(pagenum)
    else:
        raise Http404
    data = {
        'items': items,
        'pagenum': pagenum,
        'pages': [p for p in paginator.page_range],
        'firstpage': pagenum == 1,
        'lastpage': pagenum == paginator.num_pages,
        'userpage': userpage, 
        'title': title,
    }
    
    if userpage:
        user = User.objects.get(username=title)
        data['followers'] = user.followers.count()
        data['following'] = user.following.count()
        data['user_follows'] = False
        if request.user.is_authenticated:
            if request.user.following.filter(username=title).exists():
                data['user_follows'] = True
                
    return render(request, "network/index.html", data)