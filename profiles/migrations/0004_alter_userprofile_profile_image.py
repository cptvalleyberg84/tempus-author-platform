# Generated by Django 5.1.5 on 2025-02-13 12:46

import profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='media/profile_images/default.jpg', null=True, upload_to=profiles.models.profile_image_path),
        ),
    ]
