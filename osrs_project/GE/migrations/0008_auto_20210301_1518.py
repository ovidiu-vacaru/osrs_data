# Generated by Django 3.1.6 on 2021-03-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0007_auto_20210301_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemvalue',
            name='date',
            field=models.DateField(),
        ),
    ]
