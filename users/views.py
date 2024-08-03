from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, MpesaTransaction
from social.models import Post
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from decimal import Decimal
from .utils import extract_mpesa_details

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect(reverse('feed'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def is_premium(user):
    return user.is_premium and user.premium_expiry is not None and user.premium_expiry > timezone.now()


@login_required
@csrf_exempt
def purchase_premium(request):
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message')
        if not mpesa_message:
            messages.error(request, "M-Pesa message is required.")
            return render(request, 'users/purchase_premium.html')

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
                            request.user.is_verified = True
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

    return render(request, 'users/purchase_premium.html')

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
@user_passes_test(is_premium)
def premium_dashboard(request):
    # Get the search query and filter from the GET request
    query = request.GET.get('query', '')
    filter_by = request.GET.get('filter', '')

    # Get the user's posts
    user_posts = Post.objects.filter(user=request.user).select_related('user').prefetch_related('likes', 'comments')

    # Filter posts based on the search query
    if query:
        user_posts = user_posts.filter(content__icontains=query)

    # Apply sorting based on the filter
    if filter_by == 'likes':
        user_posts = user_posts.annotate(like_count=Count('likes')).order_by('-like_count')
    elif filter_by == 'comments':
        user_posts = user_posts.annotate(comment_count=Count('comments')).order_by('-comment_count')
    elif filter_by == 'views':
        user_posts = user_posts.order_by('-n_views')
    else:
        user_posts = user_posts.order_by('-created_at')

    # Calculate statistics
    total_views = sum(post.n_views for post in user_posts)
    total_likes = sum(post.likes.count() for post in user_posts)
    total_comments = sum(post.comments.count() for post in user_posts)
    
    # Get course analytics
    course_analytics = Post.objects.filter(user=request.user).values('user__course').annotate(post_count=Count('id'))
    
    context = {
        'total_posts': user_posts.count(),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'posts': user_posts,
        'query': query,
        'filter': filter_by,
        'course_analytics': list(course_analytics)
    }
    return render(request, 'users/premium_dashboard.html', context)

@login_required
def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query).distinct()
    user_data = [{'id': user.id, 'username': user.username, 'profile_picture': user.profile_picture.url if user.profile_picture else None} for user in users]
    return JsonResponse({'users': user_data})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    followers_count = user.followers.count()
    following_count = user.following.count()
    context = {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'user': user, 'form': form})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        request.user.following.add(user_to_follow)
        user_to_follow.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'profile', username=user_to_follow.username))

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if request.user != user_to_unfollow:
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'profile', username=user_to_unfollow.username))

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/settings.html', {'form': form})


@login_required
def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, 'users/user_followers.html', {
        'user': user,
        'followers': followers,
    })

@login_required
def user_following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    return render(request, 'users/user_following.html', {
        'user': user,
        'following': following,
    })