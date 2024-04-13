from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Order, OrderItem
import datetime, csv


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "order_stripe_payment",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = ["export_to_csv"]
    
    @admin.display(description="Stripe payment")
    def order_stripe_payment(self, obj):
        url = obj.get_stripe_url()
        if url:
            return mark_safe(f'<a href="{url}" target="_blank">{obj.stripe_id}</a>')
        return ""

    
    @admin.action(description="Export selected orders to CSV")
    def export_to_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta # получить метаданные модели с которой связан modeladmin
        content_disposition = f'attachment; filename={opts.verbose_name}.csv' 
        response = HttpResponse(content_type='text/csv') 
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields() if not \
        field.many_to_many and not field.one_to_many]
        writer.writerow([field.verbose_name for field in fields]) # первая строка таблицы с заголовками полей (id, name, ....)
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name) # получить значение полей из модели (obj.name, obj.id, obj.user, .....)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')  # преобразовать дату в строку если значение поля являеться датой
                data_row.append(value)
            writer.writerow(data_row) # добавить строку в таблицу
        return response

