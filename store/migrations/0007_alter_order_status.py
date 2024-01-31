# Generated by Django 4.1.3 on 2024-01-31 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_order_sold_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'В корзині'), (2, 'Оформлене покупцем'), (3, 'У процесі доставки'), (4, 'Замовлення у поштовому відділенні'), (5, 'Замовлення повернено'), (6, 'Замовлення отримано'), (7, 'Запропоновано')], default=1, verbose_name='Статус замовлення'),
        ),
    ]