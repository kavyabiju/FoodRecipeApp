# Generated by Django 4.0.2 on 2023-09-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_contact2_remove_contact_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
