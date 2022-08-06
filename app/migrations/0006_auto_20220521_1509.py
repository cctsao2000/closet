# Generated by Django 3.2 on 2022-05-21 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_clothe_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothe',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.company'),
        ),
        migrations.AlterField(
            model_name='clothe',
            name='type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.type'),
        ),
    ]