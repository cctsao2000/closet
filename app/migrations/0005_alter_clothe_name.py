# Generated by Django 3.2 on 2022-05-21 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220521_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothe',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]