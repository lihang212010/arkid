# Generated by Django 3.1.6 on 2021-03-01 07:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '0006_auto_20210220_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128)),
                ('url', models.CharField(blank=True, max_length=1024)),
                ('logo', models.FileField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tenant.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]