from django.contrib import admin
from .models import Order, OrderItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin for managing order items within the order admin interface.
    """
    model = OrderItem
    fields = ('product', 'quantity', 'price',)
    readonly_fields = ('price',)
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        """
        Make product field readonly for existing orders.
        """
        if obj:
            return ['product', 'price']
        return ['price']


class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing customer orders.
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('id', 'total_amount', 'order_date')

    fieldsets = (
        ('Order Information', {
            'fields': (
                'id',
                'user',
                'order_date',
                'total_amount',
                'payment_status'
            )
        }),
        ('Customer Information', {
            'fields': (
                'full_name',
                'email',
                'phone_number'
            )
        }),
        ('Billing Address', {
            'fields': (
                'billing_address1',
                'billing_address2',
                'billing_city',
                'billing_postcode',
                'billing_country'
            )
        })
    )

    list_display = (
        'id',
        'full_name',
        'email',
        'total_amount',
        'order_date',
        'payment_status'
    )

    list_filter = ('payment_status',)

    search_fields = (
        'full_name',
        'email',
        'billing_postcode'
    )

    ordering = ('-order_date',)


admin.site.register(Order, OrderAdmin)
