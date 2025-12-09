from django.contrib import admin
from .models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'city')
    search_fields = ('email', 'phone')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'payment_date',
        'paid_course',  # ← ВАЖНО: не course
        'paid_lesson',  # ← и не lesson
        'amount',
        'payment_method',
    )
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('user__email',)
