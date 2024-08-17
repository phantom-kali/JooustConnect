def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
<<<<<<< HEAD
        return {"unread_notification_count": count}
    return {"unread_notification_count": 0}
=======
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
