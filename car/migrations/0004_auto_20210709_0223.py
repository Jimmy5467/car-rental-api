# Generated by Django 3.2.4 on 2021-07-08 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_car_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancel',
            name='cancelled_on',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='availability_ends',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='available_from',
            field=models.DateField(),
        ),
    ]
