from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Post, Group, Message, Notification, Comment, PostView
from .forms import UserRegistrationForm, PostForm, UserSettingsForm
from django.contrib.auth import login, get_user_model
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'socialapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserRegistrationForm()
    return render(request, 'socialapp/register.html', {'form': form})

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'socialapp/feed.html', {'posts': posts})

@login_required
def increment_view_count(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if not PostView.objects.filter(post=post, user=request.user).exists():
        post.n_views += 1
        post.save()
        PostView.objects.create(post=post, user=request.user)
    
    return JsonResponse({'n_views': post.n_views})

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
    return JsonResponse({'liked': liked, 'n_likes': post.n_likes})

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'socialapp/post_create.html', {'form': form})

@login_required
def messages(request):
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()
    
    users = []
    for conv in conversations:
        if conv['sender'] == request.user.id:
            users.append(get_user_model().objects.get(id=conv['receiver']))
        else:
            users.append(get_user_model().objects.get(id=conv['sender']))
    
    return render(request, 'socialapp/messages.html', {'users': users})


@login_required
def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query).distinct()
    user_data = [{'id': user.id, 'username': user.username, 'profile_picture': user.profile_picture.url if user.profile_picture else None} for user in users]
    return JsonResponse({'users': user_data})

@login_required
def get_messages(request, user_id):
    other_user = get_user_model().objects.get(id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    messages_data = [
        {
            'id': message.id,
            'sender': message.sender.id,
            'receiver': message.receiver.id,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        }
        for message in messages
    ]
    
    return JsonResponse({'messages': messages_data})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = get_user_model().objects.get(id=receiver_id)
        message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return JsonResponse({'status': 'success', 'message': model_to_dict(message)})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def groups(request):
    groups = request.user.groups.all()
    return render(request, 'socialapp/groups.html', {'groups': groups})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'socialapp/notifications.html', {'notifications': notifications})

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, 'socialapp/settings.html', {'form': form})