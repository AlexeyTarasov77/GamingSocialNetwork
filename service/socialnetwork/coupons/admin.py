from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin for coupon model."""

    list_display = ["code", "valid_from", "valid_to", "discount", "is_expired"]
    list_filter = ["valid_from", "valid_to"]
    search_fields = ["code"]
