# Generated by Django 4.0.6 on 2022-08-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ResourceApp', '0006_order_productinorder_delete_bill_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tid',
            field=models.CharField(max_length=500, null=True),
        ),
    ]