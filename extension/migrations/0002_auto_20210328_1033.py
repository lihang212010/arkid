# Generated by Django 3.1.7 on 2021-03-28 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extension',
            name='name',
        ),
        migrations.AddField(
            model_name='extension',
            name='type',
            field=models.CharField(default='', max_length=128, verbose_name='Extension Type'),
            preserve_default=False,
        ),
    ]
