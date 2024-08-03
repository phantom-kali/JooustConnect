from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.shortcuts import get_object_or_404, render

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def poll_notifications(request):
    last_id = request.GET.get('last_id', 0)
    notifications = Notification.objects.filter(user=request.user, id__gt=last_id).order_by('id')
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({
        'notifications': [
            {
                'id': n.id,
                'content': n.content,
                'timestamp': n.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'redirect_url': n.get_redirect_url(),
            } for n in notifications
        ],
        'unread_count': unread_count
    })
