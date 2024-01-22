# Generated by Django 4.1.3 on 2024-01-22 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'В корзині'), (2, 'Замовлення здійснено'), (3, 'У процесі доставки'), (4, 'Замовлення у поштовому відділенні'), (5, 'Замовлення отримано'), (6, 'Замовлення повернено')], default=1, verbose_name='Статус замовлення'),
        ),
    ]
