# Generated by Django 4.2.2 on 2023-11-02 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_client_is_finalized_contract_paymentdetail_gloss_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='nro_operation',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]