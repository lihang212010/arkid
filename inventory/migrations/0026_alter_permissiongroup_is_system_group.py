# Generated by Django 3.2.6 on 2021-09-14 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_rename_permission_permissiongroup_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissiongroup',
            name='is_system_group',
            field=models.BooleanField(default=True, verbose_name='是否是系统组'),
        ),
    ]
