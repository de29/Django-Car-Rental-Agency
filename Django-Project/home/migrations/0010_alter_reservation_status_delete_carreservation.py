# Generated by Django 4.1.9 on 2023-05-26 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_carreservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(default='En cours', max_length=20),
        ),
        migrations.DeleteModel(
            name='CarReservation',
        ),
    ]
