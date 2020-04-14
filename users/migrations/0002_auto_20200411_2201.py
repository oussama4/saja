# Generated by Django 2.2.11 on 2020-04-11 22:01

from django.db import migrations, models
import users.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='addr',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='', max_length=40, verbose_name='ville'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='line1',
            field=models.CharField(default='', help_text='appartement, suite, unité, etc', max_length=100, verbose_name='adresse 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='line2',
            field=models.CharField(default='', help_text='adresse postale, boîte postale, etc', max_length=100, verbose_name='adresse 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=users.fields.MAPostalCodeField(blank=True, max_length=5, null=True, verbose_name='code postal'),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=users.fields.PhoneNumberField(max_length=40, verbose_name='numéro de téléphone'),
        ),
    ]