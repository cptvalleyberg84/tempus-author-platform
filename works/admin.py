from django.contrib import admin
from .models import Category, Product, Review


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing product categories.
    """
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing products/works.
    """
    list_display = (
        'name',
        'category',
        'price',
    )
    readonly_fields = (
        'created_date',
        'updated_date',
    )
    list_filter = (
        'category',
        'created_date',
    )
    ordering = (
        'category',
        'name',
        '-created_date',
        '-updated_date',
    )
    search_fields = (
        'name',
        'description',
        'friendly_name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for managing product reviews.
    """
    list_display = ('product', 'user', 'rating', 'created_date', 'approved')
    list_filter = ('approved', 'created_date', 'rating')
    search_fields = ('product__name', 'user__username', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        """
        Bulk action to approve selected reviews.
        """
        queryset.update(approved=True)
    approve_reviews.short_description = "Approve selected reviews"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
