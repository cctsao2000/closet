# Generated by Django 3.2 on 2022-07-11 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_secondhandpost_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionlog',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
