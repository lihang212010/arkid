# Generated by Django 3.2.6 on 2021-09-14 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_alter_permissiongroup_is_system_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='permissions_groups',
            field=models.ManyToManyField(blank=True, related_name='permission_groups_set', related_query_name='permission_groups', to='inventory.PermissionGroup'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions_group',
            field=models.ManyToManyField(blank=True, related_name='user_permission_groups_set', related_query_name='user_permission_groups', to='inventory.PermissionGroup'),
        ),
    ]
