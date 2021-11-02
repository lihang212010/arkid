# Generated by Django 2.2.10 on 2021-07-22 07:56

from django.db import migrations, models
import django.db.models.deletion
import oneid_meta.models.config
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('oneid_meta', '0081_auto_20210204_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('is_show', models.BooleanField(blank=True, default=True, max_length=225, verbose_name='is_show')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contacts_config', to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, oneid_meta.models.config.SingletonConfigMixin),
        ),
    ]