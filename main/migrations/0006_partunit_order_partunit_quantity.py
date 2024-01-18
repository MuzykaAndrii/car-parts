# Generated by Django 4.1.3 on 2024-01-18 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('main', '0005_partunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='partunit',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.order', verbose_name='Замовлення'),
        ),
        migrations.AddField(
            model_name='partunit',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Кількість'),
        ),
    ]
