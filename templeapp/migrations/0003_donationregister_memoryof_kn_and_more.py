# Generated by Django 4.2.7 on 2024-01-17 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templeapp', '0002_donationregister_donorname_kn'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationregister',
            name='memoryof_kn',
            field=models.CharField(default='kannadamemoryof', max_length=50),
        ),
        migrations.AlterField(
            model_name='donationregister',
            name='memoryof',
            field=models.CharField(default='', max_length=50),
        ),
    ]
