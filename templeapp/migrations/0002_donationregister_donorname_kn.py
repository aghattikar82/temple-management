# Generated by Django 4.2.7 on 2024-01-17 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationregister',
            name='donorname_kn',
            field=models.CharField(default='kannada', max_length=50),
        ),
    ]