# Generated by Django 3.2.4 on 2021-07-01 19:37

import car.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=128)),
                ('seats', models.IntegerField(default=4, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('car_type', models.CharField(max_length=128)),
                ('fuel', models.CharField(max_length=16)),
                ('rent', models.FloatField()),
                ('number_plate', models.CharField(error_messages={'unique': 'The car exist in database already.'}, max_length=16, unique=True)),
                ('issue', models.TextField(blank=True, error_messages={'max_length': 'message length must be less then 250'}, max_length=256, null=True)),
                ('city', models.CharField(max_length=64)),
                ('pickup_address', models.TextField()),
                ('drop_address', models.TextField()),
                ('is_verified', models.BooleanField(blank=True, null=True)),
                ('available_from', models.DateTimeField(default=datetime.datetime(2021, 7, 1, 19, 36, 59, 480233, tzinfo=utc))),
                ('availability_ends', models.DateTimeField()),
                ('rc_number', models.CharField(max_length=16)),
                ('AC', models.BooleanField()),
                ('AorM', models.BooleanField()),
                ('front_image', models.ImageField(blank=True, null=True, upload_to=car.models.content_file_name)),
                ('back_image', models.ImageField(blank=True, null=True, upload_to=car.models.content_file_name)),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('feedback', models.TextField(blank=True, max_length=30, null=True)),
                ('carId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car')),
            ],
        ),
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelled_on', models.DateTimeField(default=datetime.datetime(2021, 7, 1, 19, 36, 59, 480233, tzinfo=utc))),
                ('carId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car')),
                ('renterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payable_amount', models.FloatField()),
                ('start_date', models.DateTimeField(default=datetime.datetime(2021, 7, 1, 19, 36, 59, 480233, tzinfo=utc))),
                ('end_date', models.DateTimeField()),
                ('payment_status', models.BooleanField(blank=True, default=False, null=True)),
                ('owner_phone', models.CharField(max_length=10)),
                ('renter_phone', models.CharField(max_length=10)),
                ('booked_on', models.DateTimeField(default=datetime.datetime(2021, 7, 1, 19, 36, 59, 480233, tzinfo=utc))),
                ('carId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car')),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_ownerId', to=settings.AUTH_USER_MODEL)),
                ('renterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_renterId', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
