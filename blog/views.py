from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post
from blog.forms import PostForm
from django.utils import timezone
import datetime

# Create your views here.


def postList(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date").reverse()
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
            post.published_date = timezone.now()
            post.save()
            return redirect("postDetail", pk=post.pk)
        else:
            return redirect("postNew")
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
            post.published_date = timezone.now()
            post.save()
            return redirect("postDetail", pk=post.pk)
        else:
            return redirect("postEdit", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {
            'form': form
        }
        return render(request, 'blog/post_edit.html', context)
