# Generated by Django 5.1.5 on 2025-01-30 18:48

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, default='profile_images/default.jpg', null=True, upload_to='profile_images')),
                ('profile_bio', models.TextField(blank=True, max_length=500)),
                ('profile_full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profile_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_address1', models.CharField(max_length=255)),
                ('profile_address2', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_city', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_postcode', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Postcode must be 4-6 characters. Only letters and numbers', regex='^[A-Za-z0-9]{4,6}$')])),
                ('profile_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('profile_created', models.DateTimeField(auto_now_add=True)),
                ('profile_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
