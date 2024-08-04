from django.contrib import admin
from .models import User, MpesaTransaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'email', 'course', 'year', 'profile_picture')
    search_fields = ('username', 'nickname', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'phone_number','transaction_date')
    search_fields = ('transaction_id', 'phone_number', 'amount')
    list_filter = ('transaction_date', 'amount')
    ordering = ('-transaction_date',)

