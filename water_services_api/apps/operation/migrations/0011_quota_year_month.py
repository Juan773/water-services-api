# Generated by Django 4.2.2 on 2023-11-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0010_client_date_finalized_contract_client_date_retired'),
    ]

    operations = [
        migrations.AddField(
            model_name='quota',
            name='year_month',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]