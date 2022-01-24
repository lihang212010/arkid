# Generated by Django 3.2.10 on 2022-01-14 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant', '0031_auto_20211231_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeChatWorkScanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('work_user_id', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='user_id')),
                ('access_token', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='access_token')),
                ('device_id', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='设备id')),
            ],
        ),
        migrations.CreateModel(
            name='WeChatWorkScanUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('work_user_id', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='openid')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenant.tenant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='wechatworkscan_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]