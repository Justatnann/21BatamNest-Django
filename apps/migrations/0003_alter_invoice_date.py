# Generated by Django 5.0.4 on 2024-05-27 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_event_payment_method_remove_product_quantity_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.CharField(max_length=100),
        ),
    ]