# Generated by Django 3.2.7 on 2023-07-12 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_bid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryName',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
