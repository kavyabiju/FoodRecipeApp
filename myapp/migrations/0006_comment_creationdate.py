# Generated by Django 4.1.7 on 2023-09-04 13:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_comment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='creationdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]