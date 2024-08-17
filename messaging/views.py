import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Message
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from notifications.models import Notification


@login_required
def get_messages(request, user_id):
    other_user = get_user_model().objects.get(id=user_id)
    messages = Message.objects.filter(
<<<<<<< HEAD
        (Q(sender=request.user) & Q(receiver=other_user))
        | (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("timestamp")

    messages_data = [
        {
            "id": message.id,
            "sender": message.sender.id,
            "receiver": message.receiver.id,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        }
        for message in messages
    ]

    return JsonResponse({"messages": messages_data})


@login_required
def poll_messages(request, user_id):
    last_id = request.GET.get("last_id", 0)
    try:
        last_id = int(last_id)
    except ValueError:
        return JsonResponse({"error": "Invalid last_id"}, status=400)

    messages = (
        Message.objects.filter(id__gt=last_id)
        .filter(
            Q(sender=request.user, receiver_id=user_id)
            | Q(sender_id=user_id, receiver=request.user)
        )
        .order_by("id")
    )

    data = [
        {
            "id": msg.id,
            "content": msg.content,
            "sender": msg.sender.id,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data})

=======
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
def poll_messages(request, user_id):
    last_id = request.GET.get('last_id', 0)
    try:
        last_id = int(last_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid last_id'}, status=400)

    messages = Message.objects.filter(
        id__gt=last_id
    ).filter(
        Q(sender=request.user, receiver_id=user_id) | 
        Q(sender_id=user_id, receiver=request.user)
    ).order_by('id')

    data = [{
        'id': msg.id, 
        'content': msg.content, 
        'sender': msg.sender.id, 
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages]

    return JsonResponse({'messages': data})
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

def create_message_notification(user, message_type, related_id, sender_name):
    content = f"New message from {sender_name}"
    Notification.objects.create(
        user=user,
        content=content,
        notification_type=message_type,
<<<<<<< HEAD
        related_id=related_id,
    )


@csrf_exempt
@login_required
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            receiver_id = data.get("receiver_id")
            if content and receiver_id:
                receiver = User.objects.get(
                    id=receiver_id
                )  # Get the receiver user object
                message = Message.objects.create(
                    sender=request.user, receiver_id=receiver_id, content=content
                )
                # Create notification for the receiver
                create_message_notification(
                    receiver, "DM", message.id, request.user.username
                )
                return JsonResponse(
                    {
                        "status": "ok",
                        "id": message.id,
                        "timestamp": message.timestamp.isoformat(),
                    }
                )
            else:
                return JsonResponse(
                    {"status": "error", "message": "Missing content or receiver_id"},
                    status=400,
                )
        except (json.JSONDecodeError, User.DoesNotExist):
            return JsonResponse(
                {"status": "error", "message": "Invalid request"}, status=400
            )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@login_required
def messages(request, user_id=None):
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .values("sender", "receiver")
        .distinct()
    )

    users = []
    for conv in conversations:
        if conv["sender"] == request.user.id:
            users.append(get_user_model().objects.get(id=conv["receiver"]))
        else:
            users.append(get_user_model().objects.get(id=conv["sender"]))

=======
        related_id=related_id
    )

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            receiver_id = data.get('receiver_id')
            if content and receiver_id:
                receiver = User.objects.get(id=receiver_id)  # Get the receiver user object
                message = Message.objects.create(
                    sender=request.user,
                    receiver_id=receiver_id,
                    content=content
                )
                # Create notification for the receiver
                create_message_notification(receiver, 'DM', message.id, request.user.username)
                return JsonResponse({
                    'status': 'ok', 
                    'id': message.id,
                    'timestamp': message.timestamp.isoformat()
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing content or receiver_id'}, status=400)
        except (json.JSONDecodeError, User.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def messages(request, user_id=None):
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()
    
    users = []
    for conv in conversations:
        if conv['sender'] == request.user.id:
            users.append(get_user_model().objects.get(id=conv['receiver']))
        else:
            users.append(get_user_model().objects.get(id=conv['sender']))
    
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    selected_user = None
    if user_id:
        selected_user = get_user_model().objects.get(id=user_id)

<<<<<<< HEAD
    return render(
        request,
        "messaging/messages.html",
        {
            "users": users,
            "selected_user": selected_user,
        },
    )
=======
    return render(request, 'messaging/messages.html', {
        'users': users,
        'selected_user': selected_user,
    })

>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
