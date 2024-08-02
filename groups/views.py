import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMessage
from .forms import GroupForm, GroupPostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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

@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups.html', {'groups': groups})

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
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    posts = group.posts.all().order_by('-created_at')
    post_form = GroupPostForm()
    return render(request, 'groups/group_detail.html', {'group': group, 'posts': posts, 'post_form': post_form})

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
    return render(request, 'groups/group_messages.html', context)


@login_required
def poll_group_messages(request, group_id):
    last_id = request.GET.get('last_id', 0)
    try:
        last_id = int(last_id)
        group = Group.objects.get(id=group_id)
    except (ValueError, Group.DoesNotExist):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    messages = GroupMessage.objects.filter(
        id__gt=last_id,
        group=group
    ).order_by('id')

    data = [{
        'id': msg.id, 
        'content': msg.content, 
        'sender_id': msg.sender.id,
        'sender_name': msg.sender.username,
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages]

    return JsonResponse({'messages': data})

@csrf_exempt
@login_required
def send_group_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            group_id = data.get('group_id')
            if content and group_id:
                group = Group.objects.get(id=group_id)
                message = GroupMessage.objects.create(
                    sender=request.user,
                    group=group,
                    content=content
                )
                return JsonResponse({
                    'status': 'ok', 
                    'id': message.id,
                    'timestamp': message.timestamp.isoformat()
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing content or group_id'}, status=400)
        except (json.JSONDecodeError, Group.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

