# Generated by Django 3.2.7 on 2021-11-26 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0030_merge_20210930_0611'),
        ('app_market_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsubscriberecord',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='app_subscribed_records', to='tenant.tenant', verbose_name='租户'),
        ),
    ]
