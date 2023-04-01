# Generated by Django 4.1.7 on 2023-04-01 12:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_is_bought'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('percent', models.IntegerField(validators=[django.core.validators.MaxLengthValidator(100), django.core.validators.MinLengthValidator(1)])),
            ],
        ),
    ]
