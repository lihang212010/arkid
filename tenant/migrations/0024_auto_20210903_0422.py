# Generated by Django 3.2.6 on 2021-09-03 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0023_tenantdesktopconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenantprivacynotice',
            name='tenant',
        ),
        migrations.DeleteModel(
            name='TenantPasswordComplexity',
        ),
        migrations.DeleteModel(
            name='TenantPrivacyNotice',
        ),
    ]
