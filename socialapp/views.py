import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Post, Group, Message, Notification, Comment, PostView, GroupPost, GroupMessage, Report, MpesaTransaction
from .forms import UserRegistrationForm, PostForm, UserProfileForm, GroupForm, GroupPostForm
from django.contrib.auth import login, get_user_model
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from .utils import extract_mpesa_details

class MessageEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, GroupMessage):
            return {
                'content': obj.content,
                'timestamp': obj.timestamp.isoformat(),
                'sender_id': obj.sender.id,
                'sender__username': obj.sender.username,
            }
        return super().default(obj)


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


def is_premium(user):
    return user.is_premium and user.premium_expiry is not None and user.premium_expiry > timezone.now()

@login_required
def feed(request):
    posts = Post.objects.select_related('user').prefetch_related('likes', 'comments', 'views').order_by('-created_at')
    
    # Prioritize posts by premium users
    premium_posts = posts.filter(user__is_premium=True, user__premium_expiry__gt=timezone.now())
    regular_posts = posts.filter(Q(user__is_premium=False) | Q(user__premium_expiry__lte=timezone.now()))
    
    all_posts = list(premium_posts) + list(regular_posts)
    return render(request, 'socialapp/feed.html', {'posts': all_posts[:50]})  # Limit to 50 posts for performance

@login_required
@user_passes_test(is_premium)
def premium_dashboard(request):
    # Get the search query from the GET request
    query = request.GET.get('query', '')

    # Get the user's posts
    user_posts = Post.objects.filter(user=request.user)

    # Filter posts based on the search query
    if query:
        user_posts = user_posts.filter(content__icontains=query)

    # Calculate statistics based on the filtered posts
    total_views = sum(post.n_views for post in user_posts)
    total_likes = sum(post.likes.count() for post in user_posts)
    total_comments = sum(post.comments.count() for post in user_posts)
    
    context = {
        'total_posts': user_posts.count(),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'posts': user_posts,
        'query': query  # Include the query in the context to pre-fill the search box
    }
    return render(request, 'socialapp/premium_dashboard.html', context)


def premium_status(request):
    if request.user.is_authenticated:
        is_premium = request.user.is_premium and request.user.premium_expiry is not None and request.user.premium_expiry > timezone.now()
        days_left = (request.user.premium_expiry - timezone.now()).days if is_premium else 0
        return {
            'is_premium': is_premium,
            'premium_days_left': days_left
        }
    return {'is_premium': False, 'premium_days_left': 0}

@login_required
@user_passes_test(is_premium)
def post_viewers(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
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
    return render(request, 'socialapp/post_viewers.html', context)

@login_required
@csrf_exempt
def purchase_premium(request):
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message')
        if not mpesa_message:
            messages.error(request, "M-Pesa message is required.")
            return render(request, 'socialapp/purchase_premium.html')

        transaction_id, amount, transaction_date, phone_number = extract_mpesa_details(mpesa_message, action='verify')

        if transaction_id and amount and transaction_date and phone_number:
            # Check if the amount paid matches the premium subscription fee
            premium_fee = Decimal('200.00')  # Set your premium fee here
            if amount == premium_fee:
                try:
                    transaction = MpesaTransaction.objects.get(transaction_id=transaction_id)
                    if not transaction.is_used:
                        if transaction.amount == amount and transaction.phone_number == phone_number:
                            transaction.is_used = True
                            transaction.user = request.user
                            transaction.save()

                            request.user.is_premium = True
                            if request.user.premium_expiry and request.user.premium_expiry > timezone.now():
                                # If the user is renewing, add 30 days to their current expiry date
                                request.user.premium_expiry += timezone.timedelta(days=30)
                            else:
                                # For new subscriptions or expired ones, set a new 30-day period
                                request.user.premium_expiry = timezone.now() + timezone.timedelta(days=30)
                            request.user.save()

                            messages.success(request, "Premium subscription activated successfully!")
                            return redirect('premium_dashboard')
                        else:
                            messages.error(request, "Transaction details do not match our records.")
                    else:
                        messages.error(request, "This transaction has already been used.")
                except MpesaTransaction.DoesNotExist:
                    messages.error(request, "Transaction not found in our records.")
            else:
                messages.error(request, f"The amount paid (Ksh {amount}) does not match the required fee (Ksh {premium_fee}).")
        else:
            messages.error(request, "Invalid M-Pesa message. Please check and try again.")

    is_renewal = is_premium(request.user)
    context = {
        'is_renewal': is_renewal,
        'premium_fee': 200.00,
    }

    return render(request, 'socialapp/purchase_premium.html')

@csrf_exempt
@require_POST
def add_mpesa_transaction(request):
    mpesa_message = request.POST.get('mpesa_message')
    if not mpesa_message:
        return JsonResponse({'error': 'M-Pesa message is required'}, status=400)
    
    transaction_id, amount, transaction_date, phone_number = extract_mpesa_details(mpesa_message, action='add')
    
    if transaction_id and amount and transaction_date and phone_number:
        transaction, created = MpesaTransaction.objects.get_or_create(
            transaction_id=transaction_id,
            defaults={
                'amount': amount,
                'phone_number': phone_number,
                'transaction_date': transaction_date
            }
        )
        
        if created:
            return JsonResponse({'message': 'Transaction added successfully'})
        else:
            return JsonResponse({'message': 'Transaction already exists'})
    else:
        return JsonResponse({'error': 'Invalid M-Pesa message'}, status=400)

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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if is_premium(request.user):
                post.is_boosted = True
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'socialapp/post_create.html', {'form': form})


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    report_type = request.POST.get('report_type')
    description = request.POST.get('description', '')

    report = Report.objects.create(
        reporter=request.user,
        post=post,
        report_type=report_type,
        description=description
    )

    return JsonResponse({'status': 'success', 'message': 'Post reported successfully'})


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
    groups = Group.objects.all()
    return render(request, 'socialapp/groups.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['name']
            if Group.objects.filter(name=group_name).exists():
                form.add_error('name', 'There is a group with similar name.')
            else:
                group = form.save(commit=False)
                group.save()
                group.members.add(request.user)
                group.admins.add(request.user)
                return redirect('groups')

    else:
        form = GroupForm()
    return render(request, 'socialapp/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    posts = group.posts.all().order_by('-created_at')
    post_form = GroupPostForm()
    return render(request, 'socialapp/group_detail.html', {'group': group, 'posts': posts, 'post_form': post_form})

@login_required
@require_POST
def add_group_post(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    form = GroupPostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.group = group
        post.user = request.user
        post.save()
        return redirect('group_detail', group_id=group.id)
    return redirect('group_detail', group_id=group.id)

@login_required
def group_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = group.messages.all().order_by('-timestamp')[:100]  # Get last 100 messages
    messages = reversed(messages)
    members = group.members.all()
    
    # Serialize messages
    messages_json = json.dumps(list(messages), cls=MessageEncoder)
    
    context = {
        'group': group,
        'messages_json': messages_json,
        'members': members,
    }
    return render(request, 'socialapp/group_messages.html', context)

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'socialapp/notifications.html', {'notifications': notifications})

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    data = [{
        'id': n.id,
        'content': n.content,
        'timestamp': n.timestamp.isoformat(),
        'is_read': n.is_read
    } for n in notifications]
    return JsonResponse({'notifications': data})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'socialapp/settings.html', {'form': form})