# Generated by Django 3.0.8 on 2020-10-07 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
