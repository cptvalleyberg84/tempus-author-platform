# Generated by Django 5.1.5 on 2025-02-04 06:33

import blog.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(help_text='Title of the post', max_length=200, unique=True, validators=[blog.models.validate_not_empty])),
                ('post_slug', models.SlugField(help_text='URL-friendly version of the title', max_length=200, unique=True)),
                ('post_featured_image', models.ImageField(blank=True, help_text='Featured image for the blog post', null=True, upload_to='blog/featured_images/%Y/')),
                ('post_content', models.TextField(help_text='Main content of the post')),
                ('post_excerpt', models.TextField(blank=True, help_text='Brief summary of the post')),
                ('post_created_on', models.DateTimeField(auto_now_add=True)),
                ('post_updated_at', models.DateTimeField(auto_now=True)),
                ('post_status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0, help_text='0: Draft, 1: Published')),
                ('post_author', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-post_created_on'],
            },
        ),
    ]
