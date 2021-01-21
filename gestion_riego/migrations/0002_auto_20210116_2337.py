# Generated by Django 3.1.1 on 2021-01-16 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_riego', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialriego',
            name='image_1_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy1/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='historialriego',
            name='image_3_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy3/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='historialriego',
            name='image_4_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy4/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='historialriego',
            name='tiempo_riego_1_variable',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='historialriego',
            name='tiempo_riego_4_variable',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
    ]
