# Generated by Django 4.1.9 on 2023-05-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_client_address_voiture_available_voiture_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voiture',
            name='rental_rate',
        ),
        migrations.AddField(
            model_name='voiture',
            name='prix',
            field=models.IntegerField(default=2500),
        ),
        migrations.AlterField(
            model_name='voiture',
            name='color',
            field=models.CharField(default='Black', max_length=50),
        ),
        migrations.AlterField(
            model_name='voiture',
            name='description',
            field=models.TextField(default='Good Car'),
        ),
    ]