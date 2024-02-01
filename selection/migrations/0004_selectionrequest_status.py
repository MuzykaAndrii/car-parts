# Generated by Django 4.1.3 on 2024-02-01 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0003_selectionrequest_requested_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectionrequest',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Очікує підбору'), (2, 'Підбір отримано'), (3, 'Підбір прийнято'), (4, 'Підбір відхилено')], default=1, verbose_name='Статус підбору'),
        ),
    ]
