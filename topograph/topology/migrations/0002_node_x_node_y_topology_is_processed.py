# Generated by Django 4.0.4 on 2022-05-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topology', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='x',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='node',
            name='y',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='topology',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
