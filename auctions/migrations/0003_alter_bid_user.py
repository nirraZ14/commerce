# Generated by Django 3.2.7 on 2023-07-12 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20230615_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBid', to='auctions.user'),
        ),
    ]
