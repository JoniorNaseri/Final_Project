# Generated by Django 4.2.3 on 2024-06-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_alter_trade_lot_alter_trade_profit_or_loss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
