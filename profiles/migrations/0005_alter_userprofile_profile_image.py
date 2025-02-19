# Generated by Django 5.1.5 on 2025-02-13 14:36

import profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.jpg', null=True, upload_to=profiles.models.profile_image_path),
        ),
    ]
