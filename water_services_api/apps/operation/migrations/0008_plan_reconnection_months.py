# Generated by Django 4.2.2 on 2023-11-04 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0007_payment_month_payment_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='reconnection_months',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]