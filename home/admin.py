from django.contrib import admin
from .models import CarouselItem


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'style',
        'order',
        'is_active',
    )

    list_filter = ('is_active', 'style')
    search_fields = ('title',)

    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('title', 'style'),
                'subtitle',
                'description',
                'image',
                'alt_text',
            )
        }),
        ('Link Settings', {
            'description': 'Choose one of the following link types (optional)',
            'fields': (
                'product',
                'blog_post',
                'external_link',
                'open_in_new_tab',
            )
        }),
        ('Display Settings', {
            'fields': (
                'order',
                'is_active',
                'start_date',
                'end_date',
            )
        }),
    )

    ordering = ('order',)
    list_editable = ('order', 'is_active')
