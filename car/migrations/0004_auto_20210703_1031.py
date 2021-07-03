# Generated by Django 3.2.4 on 2021-07-03 05:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_auto_20210702_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked',
            name='booked_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 3, 5, 1, 28, 691605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='booked',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 3, 5, 1, 28, 691605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cancel',
            name='cancelled_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 3, 5, 1, 28, 691605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='car',
            name='available_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 3, 5, 1, 28, 691605, tzinfo=utc), null=True),
        ),
    ]
