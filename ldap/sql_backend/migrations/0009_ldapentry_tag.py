# Generated by Django 2.0.13 on 2019-11-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_backend', '0008_user_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldapentry',
            name='tag',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
