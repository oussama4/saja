# Generated by Django 2.2.11 on 2020-04-09 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='best_title',
            field=models.CharField(max_length=100, null=True, verbose_name='titre de groupe'),
        ),
    ]
