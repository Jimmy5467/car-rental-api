# Generated by Django 3.2.4 on 2021-07-08 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booked',
            name='company',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
