# Generated by Django 2.2.6 on 2021-04-07 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210407_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='account',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='currency',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]
