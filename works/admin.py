from django.contrib import admin
from .models import Category, Product

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
