# Generated by Django 3.2.10 on 2022-01-19 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0032_add_default_tenant_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='copyright_text',
            field=models.CharField(blank=True, max_length=128, verbose_name='登录页版权文字'),
        ),
    ]