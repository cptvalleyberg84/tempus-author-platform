from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
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
        if obj.post_featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.post_featured_image.url
            )
        return "No Image"

    preview_image.short_description = 'Featured Image'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.post_author = request.user
        super().save_model(request, obj, form, change)
