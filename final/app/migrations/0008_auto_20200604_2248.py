# Generated by Django 3.0.3 on 2020-06-04 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200604_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated_on',
            field=models.DateField(default=datetime.datetime(2020, 6, 4, 22, 48, 32, 290434)),
        ),
    ]
