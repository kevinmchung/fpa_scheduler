# Generated by Django 3.0.8 on 2020-07-21 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20200721_1826'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Office',
            new_name='Location',
        ),
        migrations.AlterField(
            model_name='provider',
            name='num_work_days',
            field=models.IntegerField(default=0),
        ),
    ]