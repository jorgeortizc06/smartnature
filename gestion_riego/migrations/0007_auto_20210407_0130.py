# Generated by Django 3.1.1 on 2021-04-07 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_riego', '0006_auto_20210118_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='tipo_logica_difusa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.tipologicadifusa'),
        ),
        migrations.AlterField(
            model_name='historialriego',
            name='siembra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.siembra'),
        ),
        migrations.AlterField(
            model_name='historialriego',
            name='tipo_logica_difusa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.tipologicadifusa'),
        ),
        migrations.AlterField(
            model_name='historialriego',
            name='tipo_rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.tiporol'),
        ),
        migrations.AlterField(
            model_name='plataforma',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.device'),
        ),
        migrations.AlterField(
            model_name='plataforma',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.persona'),
        ),
        migrations.AlterField(
            model_name='plataforma',
            name='tipo_suelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.tiposuelo'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.device'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='tipo_sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.tiposensor'),
        ),
        migrations.AlterField(
            model_name='siembra',
            name='planta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.planta'),
        ),
        migrations.AlterField(
            model_name='siembra',
            name='plataforma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_riego.plataforma'),
        ),
    ]