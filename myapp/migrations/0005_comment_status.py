# Generated by Django 4.1.7 on 2023-09-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.CharField(blank=True, default='Waiting For Approval', max_length=200, null=True),
        ),
    ]
