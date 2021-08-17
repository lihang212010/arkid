# Generated by Django 3.2.6 on 2021-08-17 11:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0021_merge_20210817_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantLogConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('data', models.JSONField(blank=True, default=dict)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenant.tenant', verbose_name='租户')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
