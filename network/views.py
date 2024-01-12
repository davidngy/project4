from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
import json
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    all_posts = Post.objects.all().order_by('-date', '-time')
    user = request.user

    paginator = Paginator(all_posts, 10)
    pageNumber = request.GET.get("page")
    rightPage = paginator.get_page(pageNumber)

    for post in rightPage:
        # Check if the current user has liked this post
        post.liked = post.likes.filter(pk=user.pk).exists()
        # Check if the current user is the creator of this post
        post.is_creator = (user == post.creator)

    

    return render(request, "network/index.html", {
        "allPosts": all_posts,
        "rightPage": rightPage
    })


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

@login_required
def create_post(request):
    if request.method == "POST":
        post_content = request.POST.get('post_content')
        date = timezone.now().date()
        time = timezone.now().time()
        likes_count = 0
        creator = request.user

        newPost = Post (
            post_content=post_content,
            date=date,
            time=time,
            likes_count=likes_count,
            creator=creator
        )
        newPost.save()

        return HttpResponseRedirect(reverse(index))



def like_toggle(request, postID):
    post = get_object_or_404(Post, pk=postID)
    user = request.user

    # Update whether the post is liked or not
    if request.method == "POST":
        data = json.loads(request.body)
        liked = data.get("liked")


        if liked is not None:
            print(f"postID: {postID}, liked: {liked}")
            
            # Check if the user has already liked the post
            user_has_liked = post.likes.filter(pk=user.pk).exists()

            # Toggle liked status
            liked = not user_has_liked

            if liked and not user_has_liked:
                # Like the post
                post.likes.add(user)
                post.likes_count += 1
            elif not liked and user_has_liked:
                # Unlike the post
                post.likes.remove(user)
                post.likes_count -= 1

            post.save()
            return JsonResponse({"liked": post.likes.filter(pk=user.pk).exists(), "likes_count": post.likes_count})

    # Handle other HTTP methods or invalid requests
    return HttpResponse(status=400)



def edit(request, postID):
    # Get the post object or return a 404 response if not found
    post = get_object_or_404(Post, pk=postID)
    data = json.loads(request.body.decode("utf-8"))
    new_content = data.get("post_content")

    # Double check shouldnt happen
    if request.user != post.creator:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        # Get the new content from the POST parameters, defaulting to an empty string
        print('new_content:', new_content)
        # Update the post content with the new content
        post.post_content = new_content
        post.save()


        # Return a JSON response with the updated post data
        return JsonResponse({'post_content': post.post_content})


    # Return an error response for non-POST requests

    #return HttpResponseRedirect(reverse('index'))
    return HttpResponse(status=200)

def refresh_textarea(request, postID):
    post = get_object_or_404(Post, id=postID)
    if request.method == "GET":
        data = {
        'content': post.post_content,
        }
    return JsonResponse(data)


    
def follow(request):
    userFollow = request.POST.get("userFollow")
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userFollow)
    f = Follow(user_following=currentUser, user_followed=userFollowData)
    f.save()
    userID = userFollowData.id
    return HttpResponseRedirect(reverse(get_user, kwargs={'userID': userID}))
    

def unfollow(request):
    userFollow = request.POST.get("userFollow")
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userFollow)
    f = Follow.objects.get(user_following=currentUser, user_followed=userFollowData)
    f.delete()
    userID = userFollowData.id
    return HttpResponseRedirect(reverse(get_user, kwargs={'userID': userID}))

def following(request):
    user = request.user
    currentUser = User.objects.get(pk= request.user.id)
    followingPeople = Follow.objects.filter(user_following=currentUser)
    all_posts = Post.objects.all().order_by('id').reverse()

    followingPosts = []

    for post in all_posts:
        post.liked = post.likes.filter(pk=user.pk).exists()
        # Check if the current user is the creator of this post
        post.is_creator = (user == post.creator)
        for person in followingPeople:
            if person.user_followed == post.creator:
                followingPosts.append(post)

    paginator = Paginator(followingPosts, 10)
    pageNumber = request.GET.get("page")
    rightPage = paginator.get_page(pageNumber)

    return render(request, "network/following.html", {
        "rightPage": rightPage
    })

def get_user(request, userID):
    user = User.objects.get(pk=userID)
    all_posts = Post.objects.filter(creator=user).order_by('-date', '-time').reverse()

    following = Follow.objects.filter(user_following=user)
    followers = Follow.objects.filter(user_followed=user)

    paginator = Paginator(all_posts, 10)
    pageNumber = request.GET.get("page")
    rightPage = paginator.get_page(pageNumber)

    for post in rightPage:
        # Check if the current user has liked this post
        post.liked = post.likes.filter(pk=user.pk).exists()
        # Check if the current user is the creator of this post
        post.is_creator = (user == post.creator)


    try:
        ifFollowed = followers.filter(user_following=User.objects.get(pk=request.user.id))
        if len(ifFollowed) != 0:
            ifFollowed = True
        else:
            ifFollowed = False
    except:
        ifFollowed = False
    
    

    

    if request.method == "GET":
        return render(request, "network/user.html", {
            "allPosts": all_posts,
            "username": user.username,
            "rightPage": rightPage,
            "following": following,
            "followers": followers,
            "ifFollowed": ifFollowed,
            "currentUser": user
        })