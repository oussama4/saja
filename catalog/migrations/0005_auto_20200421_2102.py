# Generated by Django 2.2.11 on 2020-04-21 21:02

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_category_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default='#F8FCFF', max_length=18),
        ),
    ]
