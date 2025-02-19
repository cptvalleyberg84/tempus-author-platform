from django.contrib import admin
from .models import CarouselItem
from .forms import CarouselItemAdminForm


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    """
    Admin interface for managing carousel items on the home page.
    """
    form = CarouselItemAdminForm
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
            )
        }),
        ('Image Settings', {
            'description': (
                'Image min 1600x800 (best fit 1920x1080) for optimal display.'
            ),
            'fields': (
                'image',
                'alt_text',
            )
        }),
        ('Link Settings', {
            'description': 'Choose one of the following link types',
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
