# Generated by Django 3.2.4 on 2021-07-11 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0008_cancel_bookid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancel',
            name='carId',
        ),
    ]
