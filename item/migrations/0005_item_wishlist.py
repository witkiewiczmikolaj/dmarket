# Generated by Django 4.1.7 on 2023-03-31 13:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0004_review_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='wishlist',
            field=models.ManyToManyField(related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
