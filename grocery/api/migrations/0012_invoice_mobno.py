# Generated by Django 2.0.4 on 2018-05-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180430_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='mobNo',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
