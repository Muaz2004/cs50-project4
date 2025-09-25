from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def index(request):
    items = Posts.objects.all().order_by('-timestamp')
    paginator=Paginator(items,10)
    page=request.GET.get('page', 1)
    query=paginator.get_page(page)
    return render(request, "network/index.html", {"query": query})



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
    




def newpost(request):
    if request.method=='POST':
        Creator=request.user
        content = request.POST.get('content')
        Posts.objects.create(creator=Creator, newpost=content)
        return HttpResponseRedirect(reverse("index"))
    return render(request,"network/index.html")



  
def profile(request, user_id):
    user = User.objects.get(pk=user_id)  
    items = Posts.objects.filter(creator=user).order_by('-timestamp')
    paginator=Paginator(items,10)
    page=request.GET.get('page', 1)
    query=paginator.get_page(page)
    allfollower = Follow.objects.filter(following=user)
    allfollowing = Follow.objects.filter(follower=user)

    # Check if the current user follows the profile user
    try:
        checkfollow = Follow.objects.filter(follower=request.user, following=user)
        isfollow = checkfollow.exists()
    except:
        isfollow = False

    return render(request, "network/profile.html", {
        "query": query,
        "profile_user": user,
        "allfollower": allfollower,
        "allfollowing": allfollowing,
        "isfollow": isfollow
    })



def follow(request):
    
    userfollow=request.POST['userfollow']
    user = User.objects.get(pk=request.user.id)
    user1=User.objects.get(username=userfollow)
    user_id=user1.id
    Follow.objects.create(follower=user,following=user1)
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))





def unfollow(request): 
    userfollow=request.POST['userfollow']
    user = User.objects.get(pk=request.user.id) 
    user1=User.objects.get(username=userfollow)   
    user_id=user1.id
    unf=Follow.objects.get(follower=user,following=user1)
    unf.delete()
    return HttpResponseRedirect(reverse("profile", kwargs={"user_id": user_id}))



def following(request):
    user = request.user
    allfollowings = user.followers.all()
    followed = [follow.following for follow in allfollowings]
    items= Posts.objects.filter(creator__in=followed).order_by('-timestamp')
    paginator=Paginator(items,10)
    page=request.GET.get('page', 1)
    query=paginator.get_page(page)
    return render(request, "network/following.html", {"query": query})


def edit(request, post_id):
    edited = Posts.objects.get(pk=post_id)
    print(edited.creator)
    if edited.creator != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    
    if request.method == 'POST':
        content = request.POST['content']
        edited.newpost = content
        edited.save()
        return HttpResponseRedirect(reverse("profile", kwargs={"user_id": request.user.id}))
    return render(request, "network/edit.html", {"edited": edited})


def like(request, postId):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'}, status=405)

    post = get_object_or_404(Posts, pk=postId)
    user = request.user
    liked = post.liked_by.filter(id=user.id).exists()

    if liked:
        post.likes -= 1
        post.liked_by.remove(user)
        liked = False  
    else:
        post.likes += 1
        post.liked_by.add(user)
        liked = True  

    post.save()
    return JsonResponse({
        'message': 'Like toggled successfully',
        'likes': post.likes,
        'liked': liked  
    }, status=200)


def get_liked_state(request, postId):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method'}, status=405)

    post = get_object_or_404(Posts, pk=postId)
    user = request.user
    liked = post.liked_by.filter(id=user.id).exists()
    return JsonResponse({
        'liked': liked
    }, status=200)
    




   
        





