# Generated by Django 4.2.2 on 2023-11-01 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='full_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]