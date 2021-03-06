# Generated by Django 3.2.4 on 2021-07-10 04:41

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(blank=True, error_messages={'unique': 'Photo exist in database already.'}, null=True, unique=True, upload_to=accounts.models.content_file_name('profile_photo/')),
        ),
    ]
