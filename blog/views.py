from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from blog.models import Post
from blog.forms import PostForm
from blog.forms import LoginUser
from django.contrib import messages
from django.utils import timezone
import datetime

# Create your views here.


def postList(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date").reverse()
    context = {
        'posts': posts
    }
    return render(request, "blog/post_list.html", context)


def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


def postNew(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'draft' in request.POST:
                post.save()
                messages.success(request, 'Draft Saved Successful!')
            elif 'publish' in request.POST:
                post.published_date = timezone.now()
                post.save()
                messages.success(request, 'Post Published Successful!')
            return redirect("post_detail", pk=post.pk)
        else:
            messages.warning(request, 'Please fill all the required fields properly!')
            return redirect("post_new")
    else:
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'blog/post_edit.html', context)


def postEdit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'draft' in request.POST:
                post.save()
                messages.success(request, 'Draft Saved Successful!')
            elif 'publish' in request.POST:
                post.published_date = timezone.now()
                post.save()
                messages.success(request, 'Post Published Successful!')
            return redirect("post_detail", pk=post.pk)
        else:
            messages.warning(request, 'Please fill all the required fields properly!')
            return redirect("post_edit", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form
        }
        return render(request, 'blog/post_edit.html', context)


def postDelete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Post Deleted Successful!')
    return redirect("post_list")


def postDrafts(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date").reverse()
    context={
        'posts' : posts
    }
    return render(request, 'blog/post_drafts.html',context)

def postPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, 'Post Published Successful!')
    return redirect("post_list")

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username , password = password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Log in Successful!')
            return redirect('post_list')
            # A backend authenticated the credentials
        else:
            messages.warning(request, 'Wrong Username or Password!')
    form = LoginUser()
    context={
        'form' : form,
    }
    return render(request, 'blog/login.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('post_list')