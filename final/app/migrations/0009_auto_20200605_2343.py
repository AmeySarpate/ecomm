# Generated by Django 3.0.3 on 2020-06-05 18:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200604_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated_on',
            field=models.DateField(default=datetime.datetime(2020, 6, 5, 23, 43, 49, 441926)),
        ),
    ]