# Generated by Django 3.2.6 on 2021-08-18 01:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('external_idp', '0002_externalidp_order_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalidp',
            name='order_no',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='序号'),
        ),
        migrations.AlterField(
            model_name='externalidp',
            name='type',
            field=models.CharField(max_length=128, verbose_name='第三方身份源类型'),
        ),
        migrations.AlterField(
            model_name='externalidp',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='唯一标识'),
        ),
    ]
