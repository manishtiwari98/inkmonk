# Generated by Django 2.0.4 on 2018-04-30 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180430_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='unit',
        ),
        migrations.AddField(
            model_name='items',
            name='measuredIn',
            field=models.CharField(default='gram', max_length=10),
        ),
    ]
