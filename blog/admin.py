from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for managing blog posts.
    """

    summernote_fields = ('post_content',)
    list_display = (
        'post_title',
        'post_status',
        'post_created_on',
        'post_author',
        'preview_image'
    )
    list_filter = ('post_status', 'post_created_on', 'post_author')
    search_fields = ['post_title', 'post_content']
    prepopulated_fields = {'post_slug': ('post_title',)}
    date_hierarchy = 'post_created_on'
    ordering = ('-post_created_on',)

    def preview_image(self, obj):
        """
        Generates HTML for displaying post featured image preview.
        """
        if obj.post_featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.post_featured_image.url
            )
        return "No Image"

    preview_image.short_description = 'Featured Image'

    def save_model(self, request, obj, form, change):
        """
        Sets the post author to current user when creating new post.
        """
        if not change:
            obj.post_author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing blog comments.
    """

    list_display = ('author', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('author__username', 'content')
    actions = ['approve_comments', 'hide_comments']

    def approve_comments(self, request, queryset):
        """
        Action to approve selected comments.
        """
        queryset.update(active=True)

    def hide_comments(self, request, queryset):
        """
        Action to hide selected comments.
        """
        queryset.update(active=False)
