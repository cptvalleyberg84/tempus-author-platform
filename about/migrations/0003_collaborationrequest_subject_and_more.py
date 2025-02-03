# Generated by Django 5.1.5 on 2025-02-03 15:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_alter_collaborationrequest_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborationrequest',
            name='subject',
            field=models.CharField(default='Hello There!', help_text='Subject of the collaboration request (optional)', max_length=200, validators=[django.core.validators.MinLengthValidator(6, 'Subject must be at least 6 characters long')]),
        ),
        migrations.AlterField(
            model_name='collaborationrequest',
            name='collaboration_type',
            field=models.CharField(choices=[('PROJECT', 'Project Collaboration'), ('MENTORSHIP', 'Mentorship'), ('BUSINESS', 'Business Opportunity'), ('INTERVIEW', 'Interview Request'), ('WRITING', 'Writing Partnership'), ('REVIEW', 'Book Review'), ('BETA', 'Beta Reading'), ('OTHER', 'Other')], default='PROJECT', max_length=20),
        ),
        migrations.AlterField(
            model_name='collaborationrequest',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(6, 'Name must be at least 6 characters long')]),
        ),
    ]
