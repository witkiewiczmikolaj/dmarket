# Generated by Django 4.1.7 on 2023-04-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_coupon_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='percent',
            field=models.IntegerField(),
        ),
    ]
