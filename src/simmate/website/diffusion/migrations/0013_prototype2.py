# Generated by Django 3.1.5 on 2021-09-29 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diffusion', '0012_prototype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prototype2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True)),
                ('formula_reduced', models.CharField(blank=True, max_length=50, null=True)),
                ('structure', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='diffusion.materialsprojectstructure')),
            ],
        ),
    ]