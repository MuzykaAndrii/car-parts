# Generated by Django 4.1.3 on 2024-01-31 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_carproducer_options_alter_partproducer_options_and_more'),
        ('selection', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='selectionrequest',
            options={'verbose_name': 'Запит на підбір', 'verbose_name_plural': 'Запити на підбір'},
        ),
        migrations.RemoveField(
            model_name='selectionresponse',
            name='proposal',
        ),
        migrations.AlterField(
            model_name='selectionresponse',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Коментар'),
        ),
        migrations.AddField(
            model_name='selectionresponse',
            name='proposal',
            field=models.ManyToManyField(to='main.part', verbose_name='Пропозиції'),
        ),
    ]