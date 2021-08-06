# Generated by Django 3.1.5 on 2021-04-22 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diffusion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaspCalcB',
            fields=[
                ('status', models.CharField(choices=[('S', 'Scheduled'), ('C', 'Completed'), ('F', 'Failed')], default='S', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('structure_start_json', models.TextField(blank=True, null=True)),
                ('structure_midpoint_json', models.TextField(blank=True, null=True)),
                ('structure_end_json', models.TextField(blank=True, null=True)),
                ('energy_start', models.FloatField(blank=True, null=True)),
                ('energy_midpoint', models.FloatField(blank=True, null=True)),
                ('energy_end', models.FloatField(blank=True, null=True)),
                ('energy_barrier', models.FloatField(blank=True, null=True)),
                ('pathway', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='diffusion.pathway')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]