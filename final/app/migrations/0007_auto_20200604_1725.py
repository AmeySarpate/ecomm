# Generated by Django 3.0.3 on 2020-06-04 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200602_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(default=9999999999),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_on',
            field=models.DateField(default=datetime.datetime(2020, 6, 4, 17, 25, 12, 176590)),
        ),
    ]