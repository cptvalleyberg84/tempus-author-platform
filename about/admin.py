from django.contrib import admin
from .models import CollaborationRequest


@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'collaboration_type', 'status', 
        'is_read', 'created_at'
    )
    list_filter = ('collaboration_type', 'status', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Request Details', {
            'fields': ('subject', 'collaboration_type', 'message')
        }),
        ('Status Information', {
            'fields': ('status', 'is_read')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True, status='READ')
    mark_as_read.short_description = "Mark selected requests as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, status='NEW')
    mark_as_unread.short_description = "Mark selected requests as unread"
