# Generated by Django 3.2.6 on 2021-09-22 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0024_auto_20210903_0422'),
    ]

    operations = [
        # 如果有提示少use_slug,可以临时解开注释跑下(hanbin)
        # migrations.AddField(
        #     model_name='tenant',
        #     name='use_slug',
        #     field=models.BooleanField(default=True, verbose_name='是否使用Slug'),
        # ),
    ]