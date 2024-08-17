import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from notifications.models import Notification
from users.models import User
from .models import Group, GroupJoinRequest, GroupMessage, GroupPost
from .forms import GroupForm, GroupPostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Group, GroupJoinRequest
from .forms import GroupForm, GroupPostForm

from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.views.decorators.cache import cache_page


class MessageEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, GroupMessage):
            return {
                "content": obj.content,
                "timestamp": obj.timestamp.isoformat(),
                "sender_id": obj.sender.id,
                "sender__username": obj.sender.username,
            }
        return super().default(obj)


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user != group.admins.first():  # Only the creator can delete the group
        messages.error(request, "You don't have permission to delete this group.")
        return redirect("group_detail", group_id=group.id)

    if request.method == "POST":
        group.delete()
        messages.success(request, f"Group '{group.name}' has been deleted.")
        return redirect("groups")

    return render(request, "groups/delete_group.html", {"group": group})


@login_required
def remove_member(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.admins.all():
        messages.error(request, "You don't have permission to remove members.")
        return redirect("group_detail", group_id=group.id)

    user_to_remove = get_object_or_404(User, id=user_id)
    if user_to_remove == group.admins.first():
        messages.error(request, "You can't remove the group creator.")
    elif user_to_remove in group.members.all():
        group.members.remove(user_to_remove)
        if user_to_remove in group.admins.all():
            group.admins.remove(user_to_remove)
        messages.success(
            request, f"{user_to_remove.username} has been removed from the group."
        )
    else:
        messages.error(
            request, f"{user_to_remove.username} is not a member of this group."
        )

    return redirect("manage_group_requests", group_id=group.id)


@login_required
def invite_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, "You don't have permission to invite members.")
        return redirect("groups")

    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_invite = User.objects.get(username=username)
            if user_to_invite not in group.members.all():
                # Here you would typically send an invitation notification
                # For now, we'll just add them directly
                group.members.add(user_to_invite)
                messages.success(request, f"{username} has been added to the group.")
            else:
                messages.info(request, f"{username} is already a member of this group.")
        except User.DoesNotExist:
            messages.error(request, f"User {username} not found.")

    return redirect("group_detail", group_id=group.id)


@login_required
@cache_page(60 * 15)  # Cache the page for 15 minutes
def groups(request):
    query = request.GET.get("q")
    category = request.GET.get("category")

    groups = (
        Group.objects.filter(
            Q(visibility="public") | Q(members=request.user) | Q(admins=request.user)
        )
        .distinct()
        .annotate(member_count=Count("members"))
    )

    if query:
        groups = groups.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
        )

    if category:
        groups = groups.filter(category=category)

    # Apply prefetch_related after all filters
    groups = groups.prefetch_related(
        Prefetch(
            "posts",
            queryset=GroupPost.objects.order_by("-created_at")[:3],
            to_attr="recent_posts",
        )
    )

    paginator = Paginator(groups, 4)  # Show 12 groups per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Group.objects.values_list("category", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "selected_category": category,
    }
    return render(request, "groups/groups.html", context)


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)
            group.admins.add(request.user)
            return redirect("groups")
    else:
        form = GroupForm()
    return render(request, "groups/create_group.html", {"form": form})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.visibility == "secret" and request.user not in group.members.all():
        return redirect("groups")

    is_member = request.user in group.members.all()
    is_admin = request.user in group.admins.all()
    can_view = group.visibility == "public" or is_member

    if not can_view:
        return redirect("groups")

    posts = group.posts.all().order_by("-created_at") if is_member else []
    post_form = GroupPostForm() if is_member else None

    context = {
        "group": group,
        "posts": posts,
        "post_form": post_form,
        "is_member": is_member,
        "is_admin": is_admin,
    }
    return render(request, "groups/group_detail.html", context)


@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.visibility == "public":
        group.members.add(request.user)
        return redirect("group_detail", group_id=group.id)
    elif group.visibility == "private":
        GroupJoinRequest.objects.get_or_create(group=group, user=request.user)
        return redirect("groups")
    else:
        return redirect("groups")


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.members.all():
        group.members.remove(request.user)
        if request.user in group.admins.all():
            group.admins.remove(request.user)
    return redirect("groups")


@login_required
def manage_group_requests(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.admins.all():
        return redirect("groups")

    join_requests = group.join_requests.all()
    members = group.members.all()

    if request.method == "POST":
        action = request.POST.get("action")

        if action in ["approve", "reject"]:
            request_id = request.POST.get("request_id")
            join_request = get_object_or_404(
                GroupJoinRequest, id=request_id, group=group
            )

            if action == "approve":
                group.members.add(join_request.user)
                join_request.delete()
            elif action == "reject":
                join_request.delete()

        elif action == "promote":
            user_id = request.POST.get("user_id")
            user_to_promote = get_object_or_404(User, id=user_id)
            if (
                user_to_promote in group.members.all()
                and user_to_promote not in group.admins.all()
            ):
                group.admins.add(user_to_promote)

        elif action == "demote":
            user_id = request.POST.get("user_id")
            user_to_demote = get_object_or_404(User, id=user_id)
            if (
                user_to_demote in group.admins.all()
                and user_to_demote != group.admins.first()
            ):  # Prevent demoting the original creator
                group.admins.remove(user_to_demote)

    context = {
        "group": group,
        "join_requests": join_requests,
        "members": members,
        "admins": group.admins.all(),
    }
    return render(request, "groups/manage_requests.html", context)


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
        return redirect("group_detail", group_id=group.id)
    return redirect("group_detail", group_id=group.id)


@login_required
def group_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = group.messages.all().order_by("-timestamp")[
        :100
    ]  # Get last 100 messages
    messages = reversed(messages)
    members = group.members.all()

    # Serialize messages
    messages_json = json.dumps(list(messages), cls=MessageEncoder)

    context = {
        "group": group,
        "messages_json": messages_json,
        "members": members,
    }
    return render(request, "groups/group_messages.html", context)


@login_required
def poll_group_messages(request, group_id):
    last_id = request.GET.get("last_id", 0)
    try:
        last_id = int(last_id)
        group = Group.objects.get(id=group_id)
    except (ValueError, Group.DoesNotExist):
        return JsonResponse({"error": "Invalid request"}, status=400)

    messages = GroupMessage.objects.filter(id__gt=last_id, group=group).order_by("id")

    data = [
        {
            "id": msg.id,
            "content": msg.content,
            "sender_id": msg.sender.id,
            "sender_name": msg.sender.username,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data})


def create_message_notification(
    user, message_type, related_id, sender_name, group_name=None
):
    if message_type == "GROUP":
        content = f"New message from {sender_name} in group {group_name}"
    else:
        content = f"New message from {sender_name}"

    Notification.objects.create(
        user=user,
        content=content,
        notification_type=message_type,
        related_id=related_id,
    )


@csrf_exempt
@login_required
def send_group_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            group_id = data.get("group_id")
            if content and group_id:
                group = Group.objects.get(id=group_id)
                message = GroupMessage.objects.create(
                    sender=request.user, group=group, content=content
                )
                # Create notifications for all group members except the sender
                for member in group.members.exclude(id=request.user.id):
                    create_message_notification(
                        member, "GROUP", group.id, request.user.username, group.name
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
                    {"status": "error", "message": "Missing content or group_id"},
                    status=400,
                )
        except (json.JSONDecodeError, Group.DoesNotExist):
            return JsonResponse(
                {"status": "error", "message": "Invalid request"}, status=400
            )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@login_required
def redirect_to_group(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    if notification.notification_type == "GROUP":
        group_id = notification.related_id
        return redirect("group_messages", group_id=group_id)
    else:
        # Handle other notification types or return a default redirect
        return redirect("groups")
