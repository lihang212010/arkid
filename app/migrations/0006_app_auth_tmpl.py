# Generated by Django 3.2 on 2021-06-04 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210327_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='auth_tmpl',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
