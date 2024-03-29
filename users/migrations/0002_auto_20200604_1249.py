# Generated by Django 2.2.12 on 2020-06-04 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=64, verbose_name='ville'),
        ),
        migrations.AlterField(
            model_name='address',
            name='line1',
            field=models.CharField(help_text='appartement, suite, unité, etc', max_length=250, verbose_name='adresse 1'),
        ),
        migrations.AlterField(
            model_name='address',
            name='line2',
            field=models.CharField(help_text='adresse postale, boîte postale, etc', max_length=250, verbose_name='adresse 2'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Un utilisateur avec cet email existe déjà.'}, max_length=64, unique=True, verbose_name='adresse email'),
        ),
    ]
