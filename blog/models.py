from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField


def validate_not_empty(value):
    if not value.strip():
        raise ValidationError('This field cannot be empty or just whitespace.')


class Post(models.Model):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Published")
    )

    post_title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Title of the post",
        validators=[validate_not_empty]
    )
    post_slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly version of the title"
    )
    post_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        limit_choices_to={'is_staff': True}
    )
    post_featured_image = models.ImageField(
        upload_to='blog/featured_images/%Y/',
        help_text="Featured image for the blog post",
        blank=True,
        null=True
    )
    post_content = RichTextUploadingField(
        help_text="Main content of the post"
    )
    post_excerpt = models.TextField(
        blank=True,
        help_text="Brief summary of the post"
    )
    post_created_on = models.DateTimeField(auto_now_add=True)
    post_updated_at = models.DateTimeField(auto_now=True)
    post_status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        help_text="0: Draft, 1: Published"
    )

    class Meta:
        ordering = ['-post_created_on']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.post_title

    def save(self, *args, **kwargs):
        if not self.post_excerpt and self.post_content:
            from django.utils.html import strip_tags
            self.post_excerpt = strip_tags(self.post_content)[:150] + '...'
        super().save(*args, **kwargs)
