# Generated by Django 3.1.5 on 2021-01-17 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0002_webhook_webhookrecord'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WebHookRecord',
            new_name='WebHookSendHistory',
        ),
        migrations.AlterField(
            model_name='webhook',
            name='content_type',
            field=models.CharField(default='application/json', max_length=128),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='secret',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
