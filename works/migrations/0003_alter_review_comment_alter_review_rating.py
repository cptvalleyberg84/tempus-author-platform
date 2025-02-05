# Generated by Django 5.1.5 on 2025-02-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0002_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, help_text='Share your thought about this story (optional).', null=True, verbose_name='Review (optional)'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Rating (required)'),
        ),
    ]
