# Generated by Django 4.0.2 on 2023-09-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_comment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.CharField(blank=True, default='unread', max_length=100, null=True),
        ),
    ]
