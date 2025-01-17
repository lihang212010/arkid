# Generated by Django 3.1.7 on 2021-03-26 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0006_auto_20210220_1237'),
        ('inventory', '0007_auto_20210325_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tenant',
        ),
        migrations.AddField(
            model_name='user',
            name='tenants',
            field=models.ManyToManyField(blank=True, related_name='user_tenant_set', related_query_name='tenant', to='tenant.Tenant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='user_permission_set', related_query_name='user_permission', to='inventory.Permission'),
        ),
    ]
