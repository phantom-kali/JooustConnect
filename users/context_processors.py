from django.utils import timezone

<<<<<<< HEAD

def premium_status(request):
    if request.user.is_authenticated:
        is_premium = (
            request.user.is_premium
            and request.user.premium_expiry is not None
            and request.user.premium_expiry > timezone.now()
        )
        days_left = (
            (request.user.premium_expiry - timezone.now()).days if is_premium else 0
        )
        return {"is_premium": is_premium, "premium_days_left": days_left}
    return {"is_premium": False, "premium_days_left": 0}
=======
def premium_status(request):
    if request.user.is_authenticated:
        is_premium = request.user.is_premium and request.user.premium_expiry is not None and request.user.premium_expiry > timezone.now()
        days_left = (request.user.premium_expiry - timezone.now()).days if is_premium else 0
        return {
            'is_premium': is_premium,
            'premium_days_left': days_left
        }
    return {'is_premium': False, 'premium_days_left': 0}
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
