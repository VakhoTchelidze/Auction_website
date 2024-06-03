# Generated by Django 4.2.13 on 2024-06-01 05:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_bid_bid_alter_item_bid_end_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Actvie"),
        ),
        migrations.AlterField(
            model_name="item",
            name="bid_end_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 6, 8, 5, 24, 23, 782546, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]
