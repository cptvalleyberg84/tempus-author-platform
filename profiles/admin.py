from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_full_name', 'profile_email', 
                   'profile_phone_number', 'profile_city', 'get_profile_image')
    list_filter = ('profile_city', 'user__is_active')
    search_fields = ('user__username', 'profile_full_name', 'profile_email', 
                    'profile_phone_number', 'profile_city')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_full_name', 'profile_email', 
                      'profile_phone_number', 'profile_image', 'profile_bio')
        }),
        ('Address Information', {
            'fields': ('profile_address1', 'profile_address2', 'profile_city', 
                      'profile_postcode', 'profile_country'),
        }),
    )

    def get_profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" />', 
                             obj.profile_image.url)
        return "No Image"
    get_profile_image.short_description = 'Profile Image'
