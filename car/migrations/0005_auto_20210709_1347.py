# Generated by Django 3.2.4 on 2021-07-09 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0004_auto_20210709_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='back_image',
            field=models.ImageField(blank=True, null=True, upload_to=None),
        ),
        migrations.AlterField(
            model_name='car',
            name='front_image',
            field=models.ImageField(blank=True, null=True, upload_to=None),
        ),
    ]
