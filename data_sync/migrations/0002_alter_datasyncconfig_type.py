# Generated by Django 3.2.6 on 2021-08-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_sync', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasyncconfig',
            name='type',
            field=models.CharField(choices=[('dingding', 'Ding Ding'), ('weichat', 'Enterprise WeiChat'), ('scim', 'Scim')], max_length=32, verbose_name='Data Sync Type'),
        ),
    ]
