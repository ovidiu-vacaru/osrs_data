# Generated by Django 3.1.6 on 2021-02-26 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("GE", "0004_itemprice"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItemValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.IntegerField()),
                ("date", models.DateField()),
                ("volume", models.IntegerField()),
                (
                    "item_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="GE.item"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ItemPrice",
        ),
    ]