from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, PostView, Report
from django.db.models import Q
from .forms import PostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST


def is_premium(user):
<<<<<<< HEAD
    return (
        user.is_premium
        and user.premium_expiry is not None
        and user.premium_expiry > timezone.now()
    )


def home(request):
    return render(request, "social/home.html")


@login_required
def feed(request):
    posts = (
        Post.objects.select_related("user")
        .prefetch_related("likes", "comments", "views")
        .order_by("-created_at")
    )

    # Prioritize posts by premium users
    premium_posts = posts.filter(
        user__is_premium=True, user__premium_expiry__gt=timezone.now()
    )
    regular_posts = posts.filter(
        Q(user__is_premium=False) | Q(user__premium_expiry__lte=timezone.now())
    )

    all_posts = list(premium_posts) + list(regular_posts)
    return render(
        request, "social/feed.html", {"posts": all_posts[:50]}
    )  # Limit to 50 posts for performance
=======
    return user.is_premium and user.premium_expiry is not None and user.premium_expiry > timezone.now()

def home(request):
    return render(request, 'social/home.html')

@login_required
def feed(request):
    posts = Post.objects.select_related('user').prefetch_related('likes', 'comments', 'views').order_by('-created_at')
    
    # Prioritize posts by premium users
    premium_posts = posts.filter(user__is_premium=True, user__premium_expiry__gt=timezone.now())
    regular_posts = posts.filter(Q(user__is_premium=False) | Q(user__premium_expiry__lte=timezone.now()))
    
    all_posts = list(premium_posts) + list(regular_posts)
    return render(request, 'social/feed.html', {'posts': all_posts[:50]})  # Limit to 50 posts for performance
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
<<<<<<< HEAD
    return JsonResponse({"liked": liked, "n_likes": post.n_likes})

=======
    return JsonResponse({'liked': liked, 'n_likes': post.n_likes})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
<<<<<<< HEAD
    content = request.POST.get("content")
    comment = Comment.objects.create(post=post, user=request.user, content=content)
    return JsonResponse(
        {
            "status": "success",
            "comment": {
                "id": comment.id,
                "content": comment.content,
                "user": comment.user.username,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "n_comments": post.n_comments,
        }
    )


@login_required
def create_post(request):
    if request.method == "POST":
=======
    content = request.POST.get('content')
    comment = Comment.objects.create(post=post, user=request.user, content=content)
    return JsonResponse({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        },
        'n_comments': post.n_comments
    })

@login_required
def create_post(request):
    if request.method == 'POST':
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if is_premium(request.user):
                post.is_boosted = True
            post.save()
<<<<<<< HEAD
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "social/post_create.html", {"form": form})
=======
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/post_create.html', {'form': form})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
<<<<<<< HEAD
    return JsonResponse({"status": "success"})

=======
    return JsonResponse({'status': 'success'})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

@login_required
@require_POST
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
<<<<<<< HEAD
    report_type = request.POST.get("report_type")
    description = request.POST.get("description", "")
=======
    report_type = request.POST.get('report_type')
    description = request.POST.get('description', '')
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

    report = Report.objects.create(
        reporter=request.user,
        post=post,
        report_type=report_type,
<<<<<<< HEAD
        description=description,
    )

    return JsonResponse({"status": "success", "message": "Post reported successfully"})
=======
        description=description
    )

    return JsonResponse({'status': 'success', 'message': 'Post reported successfully'})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c


@login_required
def increment_view_count(request, post_id):
    post = get_object_or_404(Post, id=post_id)
<<<<<<< HEAD

=======
    
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    if not PostView.objects.filter(post=post, user=request.user).exists():
        post.n_views += 1
        post.save()
        PostView.objects.create(post=post, user=request.user)
<<<<<<< HEAD

    return JsonResponse({"n_views": post.n_views})

=======
    
    return JsonResponse({'n_views': post.n_views})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

@login_required
@user_passes_test(is_premium)
def post_viewers(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
<<<<<<< HEAD
    viewers = post.views.select_related("user").order_by("-viewed_at")

    # Get search query from the GET request
    query = request.GET.get("query", "")
    if query:
        viewers = viewers.filter(user__username__icontains=query)

    context = {
        "post": post,
        "viewers": viewers,
        "query": query,
    }
    return render(request, "social/post_viewers.html", context)
=======
    viewers = post.views.select_related('user').order_by('-viewed_at')
    
    # Get search query from the GET request
    query = request.GET.get('query', '')
    if query:
        viewers = viewers.filter(user__username__icontains=query)
    
    context = {
        'post': post,
        'viewers': viewers,
        'query': query,
    }
    return render(request, 'social/post_viewers.html', context)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c


@login_required
@user_passes_test(is_premium)
def post_details(request, post_id, detail_type):
    post = get_object_or_404(Post, id=post_id, user=request.user)
<<<<<<< HEAD

    if detail_type == "views":
        details = (
            PostView.objects.filter(post=post)
            .values("user__username")
            .annotate(count=Count("id"))
        )
        key = "user__username"
    elif detail_type == "likes":
        details = post.likes.values("username").annotate(count=Count("id"))
        key = "username"
    elif detail_type == "comments":
        details = (
            Comment.objects.filter(post=post)
            .values("user__username")
            .annotate(count=Count("id"))
        )
        key = "user__username"
    else:
        return JsonResponse({"error": "Invalid detail type"}, status=400)

    details_list = [{"username": item[key], "count": item["count"]} for item in details]
=======
    
    if detail_type == 'views':
        details = PostView.objects.filter(post=post).values('user__username').annotate(count=Count('id'))
        key = 'user__username'
    elif detail_type == 'likes':
        details = post.likes.values('username').annotate(count=Count('id'))
        key = 'username'
    elif detail_type == 'comments':
        details = Comment.objects.filter(post=post).values('user__username').annotate(count=Count('id'))
        key = 'user__username'
    else:
        return JsonResponse({'error': 'Invalid detail type'}, status=400)
    
    details_list = [{'username': item[key], 'count': item['count']} for item in details]
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    return JsonResponse(details_list, safe=False)
