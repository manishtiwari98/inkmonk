# Generated by Django 2.0.4 on 2018-05-02 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20180502_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authToken',
            field=models.CharField(default='59065afde11544b1b7a13f1618451b39', max_length=50),
        ),
    ]
